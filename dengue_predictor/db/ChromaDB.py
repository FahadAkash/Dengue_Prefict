import chromadb
from chromadb.config import Settings
import pandas as pd
from datetime import datetime

# Initialize ChromaDB
client = chromadb.Client(Settings(
    persist_directory="./dengue_vector_db",
    anonymized_telemetry=False
))

# Create collection for dengue cases
collection = client.get_or_create_collection(
    name="dengue_cases",
    metadata={"description": "Historical dengue case data with predictions"}
)

def add_case_to_vector_db(case_data: dict, prediction: float):
    """
    Store a dengue case with its context in vector DB
    """
    # Create semantic description
    description = f"""
    Location: {case_data['District']} - {case_data['Area']} ({case_data['AreaType']})
    Patient: Age {case_data['Age']}, Gender {'Male' if case_data['Gender']==1 else 'Female'}
    Lab Results: NS1={'Positive' if case_data['NS1']==1 else 'Negative'}, 
                 IgG={'Positive' if case_data['IgG']==1 else 'Negative'}, 
                 IgM={'Positive' if case_data['IgM']==1 else 'Negative'}
    Housing: {case_data['HouseType']}
    Risk Score: {prediction:.2%}
    Outcome: {'Dengue' if case_data.get('Outcome', 0)==1 else 'No Dengue'}
    """
    
    # Store with metadata
    collection.add(
        documents=[description],
        metadatas=[{
            "district": case_data['District'],
            "area": case_data['Area'],
            "risk_score": prediction,
            "outcome": case_data.get('Outcome', 0),
            "timestamp": datetime.now().isoformat(),
            "age": case_data['Age'],
            "ns1": case_data['NS1'],
            "igm": case_data['IgM']
        }],
        ids=[f"case_{datetime.now().timestamp()}"]
    )

def search_similar_cases(query: str, n_results: int = 5):
    """
    Find similar historical cases
    """
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results

def get_area_risk_history(district: str, area: str):
    """
    Get historical risk for specific area
    """
    results = collection.query(
        query_texts=[f"{district} {area} dengue risk"],
        where={
            "$and": [
                {"district": district},
                {"area": area}
            ]
        },
        n_results=50
    )
    
    if not results['metadatas'][0]:
        return None
    
    # Calculate statistics
    risk_scores = [m['risk_score'] for m in results['metadatas'][0]]
    outcomes = [m['outcome'] for m in results['metadatas'][0]]
    
    return {
        "area": area,
        "district": district,
        "total_cases": len(risk_scores),
        "avg_risk_score": sum(risk_scores) / len(risk_scores),
        "positive_cases": sum(outcomes),
        "positive_rate": sum(outcomes) / len(outcomes) if outcomes else 0
    }

def batch_load_dataset(df: pd.DataFrame, model):
    """
    Load entire dataset into vector DB with predictions
    """
    print(f"Loading {len(df)} cases into vector database...")
    
    for idx, row in df.iterrows():
        # Prepare features for prediction
        features = row[['Age', 'Gender', 'NS1', 'IgG', 'IgM']].values.reshape(1, -1)
        prediction = model.predict_proba(features)[0][1]
        
        case_data = {
            'Age': row['Age'],
            'Gender': row['Gender'],
            'NS1': row['NS1'],
            'IgG': row['IgG'],
            'IgM': row['IgM'],
            'Area': row['Area'],
            'District': row['District'],
            'AreaType': row['AreaType'],
            'HouseType': row['HouseType'],
            'Outcome': row.get('Outcome', 0)
        }
        
        add_case_to_vector_db(case_data, prediction)
        
        if (idx + 1) % 100 == 0:
            print(f"Processed {idx + 1} cases...")
    
    print("✅ Vector database populated successfully!")

# Example usage
if __name__ == "__main__":
    import joblib
    
    # Load model and data
    model = joblib.load("logistic_regression_model.joblib")
    df = pd.read_csv("dengue_dataset.csv")
    
    # Populate vector DB
    batch_load_dataset(df, model)
    
    # Test similarity search
    results = search_similar_cases(
        "High risk dengue case in urban area with positive NS1 and IgM"
    )
    print("\nSimilar cases found:")
    for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
        print(f"\n{doc[:200]}...")
        print(f"Risk: {meta['risk_score']:.2%}, Outcome: {meta['outcome']}")