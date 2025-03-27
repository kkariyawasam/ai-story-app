import { useState } from "react";
import axios from "axios";

function App() {
  const [prompt, setPrompt] = useState("");
  const [story, setStory] = useState("");
  const [image, setImage] = useState(null);
  const [loadingStory, setLoadingStory] = useState(false);
  const [loadingImage, setLoadingImage] = useState(false);

  // Generate Story
  const generateStory = async () => {
    setLoadingStory(true);
    setStory("");
    setImage(null);

    try {
      const response = await axios.post("http://localhost:5000/generate_story", { prompt });
      setStory(response.data.story);
    } catch (error) {
      console.error("Error generating story:", error);
    }

    setLoadingStory(false);
  };

  // Generate Image
  const generateImage = async () => {
    setLoadingImage(true);
    setImage(null);

    try {
      const response = await axios.post("http://localhost:5000/generate_image", { story });
      setImage(`data:image/png;base64,${response.data.image}`);
    } catch (error) {
      console.error("Error generating image:", error);
    }

    setLoadingImage(false);
  };

  return (
    <div style={{ textAlign: "center", padding: "20px", fontFamily: "Arial" }}>
      <h1>AI Story Generator</h1>
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter a sentence..."
        style={{ width: "60%", padding: "10px", fontSize: "16px", marginBottom: "10px" }}
      />
      <br />
      <button onClick={generateStory} disabled={loadingStory} style={{ padding: "10px", fontSize: "16px", cursor: "pointer" }}>
        {loadingStory ? "Generating..." : "Generate Story"}
      </button>

      {story && (
        <div>
          <h2>Generated Story</h2>
          <p style={{ fontSize: "18px", width: "60%", margin: "auto", lineHeight: "1.5" }}>{story}</p>
          <button onClick={generateImage} disabled={loadingImage} style={{ padding: "10px", fontSize: "16px", cursor: "pointer" }}>
            {loadingImage ? "Generating Image..." : "Generate Illustration"}
          </button>
        </div>
      )}

      {image && (
        <div>
          <h2>Generated Illustration</h2>
          <img src={image} alt="AI Illustration" style={{ width: "50%", borderRadius: "10px", marginTop: "10px" }} />
        </div>
      )}
    </div>
  );
}

export default App;
