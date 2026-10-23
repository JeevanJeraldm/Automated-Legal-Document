# Kaggle Dataset Reference for Legal Document Analyzer

## Dataset Overview
This project utilizes legal contracts and documents sourced and adapted from:
**CUAD (Contract Understanding Atticus Dataset) v1**
- **Kaggle URL**: https://www.kaggle.com/datasets/theatticusproject/cuad
- **Source**: The Atticus Project / Stanford University
- **Description**: CUAD is a curated corpus of commercial legal contracts annotated by legal professionals. It contains over 500 contracts covering 41 critical legal categories including Parties, Governing Law, Termination, Non-Compete, Obligations, Payment, and Exclusivity.

## Included Sample Documents in this Repository
1. `sample_service_agreement.txt`
   - **Type**: Professional Services & Software Development Agreement
   - **Parties**: ABC Technologies Inc. and XYZ Solutions LLC
   - **Key Clauses**: Scope of Work, Deliverables, Payment Terms ($15,000/month), Confidentiality, Term (12 Months), Termination for Convenience (30 days written notice) and Cause.
   - **Purpose**: Serves as the primary validation test case matching the lab experiment's sample output specification.

2. `sample_nda.txt`
   - **Type**: Mutual Non-Disclosure Agreement (MNDA)
   - **Parties**: Apex Innovations Corp. and Quantum Dynamics Ltd.
   - **Key Clauses**: Definition of Confidential Information, Exclusions, Non-Disclosure Obligations, Term (3 years), Return of Materials, Governing Law.

3. `sample_software_license.txt`
   - **Type**: Enterprise Software License & SaaS Agreement
   - **Parties**: CloudScale Systems Inc. and Enterprise Logistics Group
   - **Key Clauses**: Grant of License, Usage Restrictions, Subscription Fees, SLA & Support, Warranties & Indemnification, Term & Renewal.

4. `sample_commercial_lease.txt`
   - **Type**: Commercial Real Estate Lease Agreement
   - **Parties**: Metro Commercial Realty Partners (Landlord) and Horizon Retail Ventures (Tenant)
   - **Key Clauses**: Leased Premises, Rent & Security Deposit, Permitted Use, Maintenance & Alterations, Default & Eviction, Term (36 months).

5. `sample_service_agreement.pdf`
   - Formatted PDF version of the Service Agreement for validating PDF text extraction via `pypdf`.
