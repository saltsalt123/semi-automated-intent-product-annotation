# Conversation Intent and Product Annotation Tool

This project is a Python-based tool developed during my Software Engineering Internship at China Unicom. The program helps semi-automatically identify customer intentions and related telecom products from customer service conversations.

## Project Overview

Customer service conversations often contain valuable information about customer needs, service requests, and product interests. However, manually labeling these conversations is time-consuming and inefficient.

This tool automates part of the annotation process by:

- Reading customer chat messages from an Excel dataset
- Sending the messages to an API for intent and product analysis
- Returning structured outputs including:
  - Identified product
  - Customer intent
  - Confidence level
  - Explanation of the classification
- Writing the labeled results back to an Excel file for further review and analysis

## Technologies Used

- Python
- Pandas
- OpenPyXL
- REST APIs
- JSON data processing

## Key Features

- Automated conversation intent recognition
- Semi-automated product identification
- API-based analysis workflow
- Structured data processing pipeline
- Excel input/output integration

## Purpose

This project demonstrates how backend scripts and data pipelines can help automate repetitive data labeling tasks and improve efficiency in real-world business workflows.

## Author

Developed as part of a Software Engineering Internship project at China Unicom.
