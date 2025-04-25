// frontend/src/pages/UploadPage.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const UploadPage = () => {
  const [video, setVideo] = useState(null);
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);

  const handleVideoChange = (e) => {
    setVideo(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!video) {
      alert("Lütfen bir video seçin!");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("video", video);

    try {
      const result = await axios.post('http://localhost:8000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResponse(result.data);
    } catch (error) {
      console.error("Video yükleme hatası:", error);
    } finally {
      setLoading(false);
    }
  };

  // Gelen veriyi logla
  useEffect(() => {
    if (response) {
      console.log("Gelen response:", response);
    }
  }, [response]);

  return (
    <div className="upload-container">
      <h1>Toplantı Videosu Yükle</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="video/*" onChange={handleVideoChange} />
        <br />
        <button type="submit" disabled={loading}>
          {loading ? "Yükleniyor..." : "Yükle"}
        </button>
      </form>

      {response && (
        <div style={{ textAlign: "left", marginTop: "20px" }}>
          <h2>Toplantı Özeti:</h2>
          <p>{response.summary}</p>

          <h2>Transkript:</h2>
          <p style={{ whiteSpace: "pre-wrap", background: "#f9f9f9", padding: "10px", border: "1px solid #ddd", borderRadius: "8px", maxHeight: "400px", overflowY: "auto" }}>
            {response.transcription}
          </p>

          <h2>Duygu Analizi:</h2>
          <pre>{JSON.stringify(response.emotions, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default UploadPage;
