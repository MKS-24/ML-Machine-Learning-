# Placement Predictor

Structure:
  index.html        -> frontend
  api/predict.py    -> Vercel Python serverless function
  model.pkl         -> put YOUR model file here (project root)
  requirements.txt  -> scikit-learn version must match the one used to train

Deploy:
  1. Copy model.pkl into this folder
  2. Push to GitHub, then Import Project on vercel.com  (or run `vercel` via CLI)
