# Welcome to UVA API - 1.0.0

by Caio saldanha | hello@caiosaldanha.com | caiosaldanha.com

# Description

This API performs an online data retrieval of Wine, Juice and Derivative production from Brasil. 🍇

# Items

- **Production** - Production of wines, juices, and derivatives from Rio Grande do Sul

- **Processing** - Quantity of grapes processed in Rio Grande do Sul
  - Vinifera, 
  - American and Hybrid grapes
  - Table grapes
  - Unclassified

- **Commercialization** - Comertialization of wines and derivatives in Rio Grande do Sul

- **Importation** - Importation of grape derivatives
  - Table wines
  - Sparkling wines
  - Fresh grapes
  - Raisins
  - Grape juice

- **Exportation** - Exportation of grape derivatives
  - Table wines
  - Sparkling wines
  - Fresh grapes
  - Grape juice

# Usage

You will be able to:

* **Retrieve a dataframe** for each item - already with all subitems.
* **Retrieve yearly data** of each item from 1970 to 2023.

# How to run this project

1. git clone
2. cd /
3. docker-composer > uva-api

# Tech Stack

### Backend

- FastAPI - Backend API used to retrive data and return in a dataframe format ready to use

### Frontend

- Flask - Simple front end in flask

# Architecture

### Overview

- Diagram

# Folder structure

### /

- **uva-api.py** - entry point for the applicaiton

### /files

General files

- **test.http** - file to test requests with VS Code extention REST Client

### /routes

API routes

- **welcome.py** - /
- **production.py** - /api/v1/production/{year}
- **processing.py** - /api/v1/processing/{year}
- **commercialization.py** - /api/v1/commercialization/{year}
- **importation.py** - /api/v1/importation/{year}
- **exportation.py** - /api/v1/exportation/{year}

### /services

Business logic and reusable functions

- **vitibrasilscraper.py** - web scraping of vitibrasil website data

# Licesing

**Apache 2.0** - http://www.apache.org/licenses/