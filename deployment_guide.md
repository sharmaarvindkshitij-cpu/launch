# FraudShield AI - Deployment Guide

## Vercel Deployment

Deploying a Flask backend and static frontend to Vercel is highly straightforward. 

### Prerequisites
1. Create a GitHub repository and push this project's code.
2. Sign up / Log in to [Vercel](https://vercel.com).

### Step-by-Step Deployment
1. Go to your Vercel dashboard and click **Add New** > **Project**.
2. Import your GitHub repository for `FraudShield AI`.
3. Vercel will automatically detect `vercel.json` and build the Python environment based on your `requirements.txt`.
4. Click **Deploy**.

## Custom Domain Setup
1. In the Vercel project dashboard, go to **Settings** -> **Domains**.
2. Enter your custom domain (e.g., `fraudshield.ai`).
3. Vercel will provide DNS verification records (A/CNAME records).
4. Add these records in your domain registrar's DNS settings (e.g., GoDaddy, Namecheap).
5. Once propagated, Vercel will automatically provision a free SSL certificate.

## Important Note on SQLite (Serverless Environments)
Since Vercel uses a serverless read-only filesystem, SQLite will **NOT** persist data across function invocations. For a production app on Vercel, replace SQLite in `utils/db.py` with a cloud database like **Supabase**, **MongoDB Atlas**, or **Vercel Postgres**. The current implementation supports development and hackathon-style MVPs running on traditional VMs.
