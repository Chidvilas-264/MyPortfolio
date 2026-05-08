# Supabase Portfolio Setup Guide

This guide provides step-by-step instructions to set up your Supabase project and run the website locally.

## 1. Supabase Project Setup

### A. Create Tables
1.  Go to your **Supabase Dashboard** -> **SQL Editor**.
2.  Click **New Query**.
3.  Copy and paste the contents of `supabase_setup.sql` (provided below or in your project folder) and click **Run**.

### B. Create Storage Buckets
1.  Go to **Storage** in the Supabase Sidebar.
2.  Create the following buckets:
    *   `profile-assets`: Set to **Public**.
    *   `project-images`: Set to **Public**.
    *   `resumes`: Set to **Public**.
3.  *Note: Ensure "Public" toggle is ON for all buckets so images can be viewed.*

### C. Authentication (Admin User)
1.  Go to **Authentication** -> **Users**.
2.  Click **Add User** -> **Create new user**.
3.  Enter an email and password (this will be your Admin login).
4.  *Note: You may need to disable "Confirm Email" in Auth -> Settings -> Providers -> Email if you want to log in immediately without verifying.*

---

## 2. Local Development Setup

### A. Configure Environment Variables
1.  Open the `frontend/.env` file.
2.  Ensure you have the correct URL and Anon Key:
    *   `VITE_SUPABASE_URL`: Found in Settings -> API -> Project URL.
    *   `VITE_SUPABASE_ANON_KEY`: Found in Settings -> API -> `anon` `public` key. (It should be a very long string).

### B. Install & Run
1.  Open a terminal in the `frontend` directory:
    ```bash
    cd C:\Portfolio\frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```
4.  The website will be available at: `http://localhost:5173` (or the port shown in the terminal).

---

## 3. Admin Access
*   **Login URL**: `http://localhost:5173/admin/login`
*   **Credentials**: Use the email and password you created in Supabase Auth.

---

## SQL Schema (Copy this to Supabase SQL Editor)

```sql
-- 1. Create Profiles Table
CREATE TABLE IF NOT EXISTS profiles (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  "fullName" TEXT,
  title TEXT,
  bio TEXT,
  "githubLink" TEXT,
  "linkedinLink" TEXT,
  email TEXT,
  "phoneNumber" TEXT,
  profile_photo_url TEXT,
  resume_url TEXT
);

-- 2. Create Education Table
CREATE TABLE IF NOT EXISTS education (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  degree TEXT,
  institution TEXT,
  year TEXT,
  grade TEXT
);

-- 3. Create Skills Table
CREATE TABLE IF NOT EXISTS skills (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  name TEXT,
  category TEXT,
  "evidenceLink" TEXT
);

-- 4. Create Work Experience Table
CREATE TABLE IF NOT EXISTS work_experience (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  company TEXT,
  position TEXT,
  "projectName" TEXT,
  start_date DATE,
  end_date DATE,
  "workMode" TEXT,
  description TEXT,
  location TEXT,
  link TEXT,
  image_url TEXT
);

-- 5. Create Projects Table
CREATE TABLE IF NOT EXISTS projects (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  title TEXT,
  description TEXT,
  category TEXT,
  "githubLink" TEXT,
  "demoLink" TEXT,
  "techStack" TEXT,
  image_url TEXT
);

-- 6. Create Certifications Table
CREATE TABLE IF NOT EXISTS certifications (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  title TEXT,
  provider TEXT,
  date DATE,
  "verificationLink" TEXT,
  image_url TEXT
);

-- 7. Create Achievements Table
CREATE TABLE IF NOT EXISTS achievements (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  title TEXT,
  description TEXT,
  link TEXT,
  date DATE,
  image_url TEXT
);

-- 8. Create Messages Table
CREATE TABLE IF NOT EXISTS messages (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  name TEXT,
  email TEXT,
  "phoneNumber" TEXT,
  content TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```
