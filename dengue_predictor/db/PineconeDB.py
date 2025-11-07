from pinecone import Pinecone, ServerlessSpec
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import os
import hashlib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Pinecone
api_key = os.getenv("PINECONE_API_KEY")
if not api_key:
    raise ValueError("PINECONE_API_KEY environment variable not set")

# Use the correct initialization method with a free plan supported region
pc = Pinecone(api_key=api_key)
index_name = "dengue-cases"

# Create or connect to index
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # Standard dimension for text embeddings
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"  # Free plan supported region
        )
    )

index = pc.Index(index_name)

def _generate_embedding(text: str) -> List[float]:
    """
    Generate embedding for text using a simple hash-based approach
    In production, you would use a proper embedding model
    """
    # Simple hash-based embedding for demonstration
    hash_object = hashlib.md5(text.encode())
    hex_dig = hash_object.hexdigest()
    
    # Convert hash to float values between 0 and 1
    embedding = []
    for i in range(0, len(hex_dig), 4):
        chunk = hex_dig[i:i+4]
        # Convert hexadecimal to integer and normalize
        val = int(chunk, 16) / 65535.0
        embedding.append(val)
        if len(embedding) >= 1536:
            break
    
    # Pad or truncate to exact dimension
    while len(embedding) < 1536:
        embedding.append(0.0)
    
    return embedding[:1536]

def add_case_to_vector_db(case_data: dict, prediction: float):
    """
    Store a dengue case with its context in Pinecone vector DB
    """
    # Create semantic description
    description = f"""
    Location: {case_data['District']} - {case_data['Area']} ({case_data.get('AreaType', 'Unknown')})
    Patient: Age {case_data['Age']}, Gender {'Male' if case_data['Gender']==1 else 'Female'}
    Lab Results: NS1={'Positive' if case_data['NS1']==1 else 'Negative'}, 
                 IgG={'Positive' if case_data['IgG']==1 else 'Negative'}, 
                 IgM={'Positive' if case_data['IgM']==1 else 'Negative'}
    Housing: {case_data.get('HouseType', 'Unknown')}
    Risk Score: {prediction:.2%}
    Outcome: {'Dengue' if case_data.get('Outcome', 0)==1 else 'No Dengue'}
    """
    
    # Generate embedding
    embedding = _generate_embedding(description)
    
    # Create metadata
    metadata = {
        "district": case_data['District'],
        "area": case_data['Area'],
        "risk_score": prediction,
        "outcome": case_data.get('Outcome', 0),
        "timestamp": datetime.now().isoformat(),
        "age": case_data['Age'],
        "ns1": case_data['NS1'],
        "igm": case_data['IgM'],
        "description": description
    }
    
    # Store in Pinecone
    vector_id = f"case_{datetime.now().timestamp()}"
    index.upsert([(vector_id, embedding, metadata)])

def search_similar_cases(query: str, n_results: int = 5):
    """
    Find similar historical cases using Pinecone
    """
    # Generate embedding for query
    query_embedding = _generate_embedding(query)
    
    # Search in Pinecone
    results = index.query(
        vector=query_embedding,
        top_k=n_results,
        include_metadata=True
    )
    
    return results

def get_area_statistics(district: str, area: str):
    """
    Get historical risk for specific area
    """
    # Fetch vectors with specific district and area
    # Note: Pinecone doesn't support direct filtering, so we'll fetch and filter
    # This is a simplified approach - in production, you might want a separate database for stats
    
    # For now, we'll search for cases in this area and calculate stats
    query_text = f"{district} {area} dengue risk"
    results = search_similar_cases(query_text, n_results=50)
    
    if not results['matches']:
        return None
    
    # Filter results by district and area
    filtered_matches = [
        match for match in results['matches']
        if match['metadata'].get('district') == district and 
           match['metadata'].get('area') == area
    ]
    
    if not filtered_matches:
        return None
    
    # Calculate statistics
    risk_scores = [match['metadata']['risk_score'] for match in filtered_matches]
    outcomes = [match['metadata']['outcome'] for match in filtered_matches]
    
    return {
        "area": area,
        "district": district,
        "total_cases": len(risk_scores),
        "avg_risk_score": sum(risk_scores) / len(risk_scores),
        "positive_cases": sum(outcomes),
        "positive_rate": sum(outcomes) / len(outcomes) if outcomes else 0
    }

def get_high_risk_areas(threshold: float = 0.7):
    """
    Get areas with risk scores above threshold
    """
    # This is a simplified implementation
    # In practice, you might want to store aggregated statistics separately
    query_text = "high risk dengue areas"
    results = search_similar_cases(query_text, n_results=100)
    
    # Group by area and calculate average risk
    area_stats = {}
    for match in results['matches']:
        district = match['metadata'].get('district')
        area = match['metadata'].get('area')
        risk_score = match['metadata'].get('risk_score', 0)
        
        key = f"{district}-{area}"
        if key not in area_stats:
            area_stats[key] = {
                'district': district,
                'area': area,
                'risks': []
            }
        area_stats[key]['risks'].append(risk_score)
    
    # Calculate averages and filter by threshold
    high_risk_areas = []
    for key, stats in area_stats.items():
        avg_risk = sum(stats['risks']) / len(stats['risks'])
        if avg_risk >= threshold:
            high_risk_areas.append({
                'district': stats['district'],
                'area': stats['area'],
                'avg_risk_score': avg_risk,
                'case_count': len(stats['risks'])
            })
    
    # Sort by risk score
    high_risk_areas.sort(key=lambda x: x['avg_risk_score'], reverse=True)
    return high_risk_areas

def batch_load_dataset(df: pd.DataFrame, model):
    """
    Load entire dataset into vector DB with predictions
    """
    print(f"Loading {len(df)} cases into vector database...")
    
    for idx, row in df.iterrows():
        # Prepare features for prediction
        try:
            features = [[
                row['Age'],
                row['Gender'],
                row['NS1'],
                row['IgG'],
                row['IgM']
            ]]
            prediction = model.predict_proba(features)[0][1]
        except Exception as e:
            print(f"Error predicting for row {idx}: {e}")
            continue
        
        case_data = {
            'Age': row['Age'],
            'Gender': row['Gender'],
            'NS1': row['NS1'],
            'IgG': row['IgG'],
            'IgM': row['IgM'],
            'Area': row.get('Area', 'Unknown'),
            'District': row.get('District', 'Unknown'),
            'AreaType': row.get('AreaType', 'Unknown'),
            'HouseType': row.get('HouseType', 'Unknown'),
            'Outcome': row.get('Outcome', 0)
        }
        
        add_case_to_vector_db(case_data, prediction)
        
        if (idx + 1) % 100 == 0:
            print(f"Processed {idx + 1} cases...")
    
    print("✅ Vector database populated successfully!")