import axios from "axios";

const API_URL = "http://localhost:8000";  // FastAPI backend URL

export const summarizeMeeting = async (meetingId, transcript) => {
  try {
    const response = await axios.post(`${API_URL}/summarize`, { meeting_id: meetingId, transcript });
    return response.data;
  } catch (error) {
    console.error("Error summarizing meeting", error);
    return null;
  }
};