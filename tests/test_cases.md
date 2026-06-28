# FieldForm AI Test Cases

This document lists planned manual and functional test cases for FieldForm AI.

## Goal

Verify that FieldForm AI can convert unstructured form input into clean structured data while working offline on CPU.

## Parser Test Cases

| Test ID | Input Type | Scenario | Expected Result |
|---|---|---|---|
| TC-001 | Text | Form contains name, age, phone, and address | JSON output contains correct fields |
| TC-002 | Text | Form has missing optional field | Parser does not fail |
| TC-003 | Text | Form contains extra spaces and line breaks | Output is cleaned and structured |
| TC-004 | Text | Form contains unknown field names | Unknown fields are handled safely |
| TC-005 | Text | Empty input is provided | Validation error is returned |
| TC-006 | OCR Text | OCR output has spelling/noise issues | Parser extracts closest valid fields |
| TC-007 | Document Text | Long form with multiple sections | JSON groups related fields correctly |
| TC-008 | Offline Mode | Internet is turned off during processing | Core extraction still works |
| TC-009 | CPU Mode | App runs without GPU/CUDA | Inference completes on CPU |
| TC-010 | Invalid Input | Unsupported file/input is provided | Clear error message is shown |

## Manual Testing Checklist

- [ ] Upload or provide sample form input.
- [ ] Confirm text extraction works.
- [ ] Confirm parser returns structured JSON.
- [ ] Test with Wi-Fi turned off.
- [ ] Confirm no cloud API call is required.
- [ ] Verify output is readable and reusable.
- [ ] Check error handling for invalid input.