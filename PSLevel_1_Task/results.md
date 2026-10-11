# Day 8 - Agentic RAG Helpdesk Results

## Features Implemented
- Handbook retrieval using similarity search and a distance threshold.
- Course fee lookup for CS101, AI202, and DS303.
- Exam attendance eligibility checking.
- Arithmetic calculator with restricted expression evaluation.
- LangGraph agent with tool calling.
- In-memory conversation checkpointing.
- Error handling for individual agent queries.

## Test Results
1. Placement eligibility: Passed. Retrieved minimum CGPA of 6.5.
2. Attendance eligibility: Passed. Checked 70% attendance.
3. Course fee lookup: Passed. CS101 fee is Rs. 12,000.
4. Fee total: Passed. Calculated Rs. 32,000 using CS101 (Rs. 12,000), AI202 (Rs. 18,000), and an assumed maximum late fee of Rs. 2,000.
5. Off-topic question: Passed. The agent stated that the answer was unavailable in the handbook.
6. Direct tool validation: Passed. Fee lookup, arithmetic, and attendance tools executed.

## Important Note
The Rs. 2,000 maximum late fee must be verified against fee_policy.md before reporting the total as an official college fee. The execution log is saved in run_log.txt.
