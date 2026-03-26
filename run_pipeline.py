from ml_pipeline.preprocessing import load_text_datasets, prepare_text_pipeline_data, load_tabular_dataset
from ml_pipeline.train import train_and_compare
from ml_pipeline.optimize import save_model
import warnings

# Suppress sklearn/xgboost warnings for cleaner console output
warnings.filterwarnings('ignore')

def main():
    print("="*60)
    print("Starting Advanced Fraud Detection ML Pipeline")
    print("="*60)
    
    # 1. Text Modality (Messages, Emails, UPI SMS)
    print("\n--- Phase 1: Text Datasets ---")
    text_df = load_text_datasets()
    if not text_df.empty:
        X_train_t, X_test_t, y_train_t, y_test_t, vectorizer = prepare_text_pipeline_data(text_df)
        best_text_model, text_name, _ = train_and_compare(X_train_t, y_train_t, X_test_t, y_test_t, title="Text Messages & SMS")
        
        # Save
        if best_text_model:
            save_model(best_text_model, vectorizer, 'text_fraud_model')
    else:
        print("No text datasets found. Skipping Phase 1.")
        
    # 2. URL Tabular Modality
    print("\n--- Phase 2: URL & Domain Features ---")
    X_train_u, X_test_u, y_train_u, y_test_u, scaler, cols = load_tabular_dataset()
    if X_train_u is not None:
        best_url_model, url_name, _ = train_and_compare(X_train_u, y_train_u, X_test_u, y_test_u, title="Phishing URLs Framework")
        
        if best_url_model:
            save_model(best_url_model, scaler, 'url_fraud_model')
    else:
        print("No tabular URL datasets found. Skipping Phase 2.")
        
    print("\n✅ Pipeline Execution Completed Successfully.")

if __name__ == "__main__":
    main()
