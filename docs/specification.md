# FieldForm AI Specification

## 1. Project Objective

FieldForm AI is an offline-first, CPU-powered AI application that converts unstructured field inspection notes into structured JSON records using a lightweight local language model.

The primary objective is to reduce manual data entry while enabling field workers to operate completely offline.

## 2. Target Users

* Government Inspectors
* NGO Volunteers
* Survey Officers
* Municipality Staff
* Disaster Response Teams

## 3. Functional Requirements

* Accept field inspection notes as input.
* Process data locally without internet connectivity.
* Extract structured information into JSON.
* Store extracted data in a local SQLite database.
* Allow users to view saved inspection records.

## 4. Non-Functional Requirements

* Offline-first operation
* CPU-only inference
* Lightweight and fast
* Privacy-preserving local processing
* Open-source software
