let capturedImages = [];
let capturing = false;

const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const captureCountEl = document.getElementById("captureCount");
const captureProgressEl = document.getElementById("captureProgress");
const thumbsEl = document.getElementById("thumbs");
const submitBtn = document.getElementById("submitBtn");
const alertBox = document.getElementById("responseAlert");

// 1) Start camera using native getUserMedia
async function startCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
  } catch (err) {
    console.error("Camera error:", err);
    alertBox.classList.remove("d-none");
    alertBox.classList.add("alert-danger");
    alertBox.innerHTML = "Unable to access camera: " + err.message;
  }
}

startCamera();

// 2) Auto capture 30 frames
document.getElementById("startCaptureBtn").onclick = () => {
  if (capturing) return;
  capturing = true;
  capturedImages = [];
  thumbsEl.innerHTML = "";
  captureCountEl.innerText = "0";
  captureProgressEl.style.width = "0%";
  submitBtn.disabled = true;

  let count = 0;

  const interval = setInterval(() => {
    if (count >= 30) {
      clearInterval(interval);
      capturing = false;
      submitBtn.disabled = false;
      return;
    }

    // draw current video frame into canvas
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // convert to base64 jpeg
    const dataUrl = canvas.toDataURL("image/jpeg", 0.9);
    capturedImages.push(dataUrl);

    count++;
    captureCountEl.innerText = String(count);
    captureProgressEl.style.width = (count / 30 * 100) + "%";

    const img = document.createElement("img");
    img.src = dataUrl;
    img.style.width = "50px";
    img.classList.add("rounded", "border");
    thumbsEl.appendChild(img);
  }, 300);
};

// 3) Submit registration
document.getElementById("registerForm").onsubmit = (e) => {
  e.preventDefault();

  const payload = {
    student_id: document.getElementById("student_id").value,
    name: document.getElementById("name").value,
    roll_no: document.getElementById("roll_no").value,
    email: document.getElementById("email").value,
    images: capturedImages,
  };

  fetch("/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
    .then(r => r.json())
    .then(d => {
      alertBox.classList.remove("d-none", "alert-danger", "alert-success");
      alertBox.classList.add(d.status === "success" ? "alert-success" : "alert-danger");
      alertBox.innerHTML = d.message || "Saved";

      if (d.status === "success") {
        // optional: reset form
      }
    })
    .catch(err => {
      console.error(err);
      alertBox.classList.remove("d-none");
      alertBox.classList.add("alert-danger");
      alertBox.innerHTML = "Error saving registration.";
    });
};
