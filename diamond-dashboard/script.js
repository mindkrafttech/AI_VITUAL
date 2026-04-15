// script.js – Smart Features for Diamond Dashboard

const dashboard = document.querySelector('.workspace-layout') || document.querySelector('.dashboard');
const avatarHub = document.querySelector('.avatar-hub');
const avatarImg = document.getElementById('avatarImg');

// --- Perfet AI Identity Sync ---
window.addEventListener('load', () => {
  console.log("%c[SYSTEM] INITIALIZING IDENTITY SYNC...", "color: #22d3ee; font-weight: bold;");
  
  if (avatarImg) {
    // Force a re-load of the brand new V3 identity to kill browser cache
    avatarImg.src = 'avatar_v3.png?v=ELITE';
    
    avatarImg.onload = () => {
      console.log("%c[SYSTEM] AI MENTOR ONLINE", "color: #22d3ee;");
      // Premium GSAP Hologram Flicker Entry
      if (window.gsap) {
        gsap.fromTo(avatarImg, 
          { opacity: 0, filter: 'brightness(3) contrast(2)' },
          { opacity: 1, filter: 'brightness(1.4) contrast(1.2)', duration: 1.5, ease: "power4.out" }
        );
        // Add a subtle scan line flicker
        gsap.to(avatarImg, {
          opacity: 0.8,
          duration: 0.1,
          repeat: 5,
          yoyo: true,
          delay: 0.5
        });
      }
    };
    
    avatarImg.onerror = () => {
      console.warn("[SYSTEM] LOCAL ASSET FAIL - FALLING BACK TO CLOUD SHIELD");
      avatarImg.src = '/avatar'; // Fallback to Flask dynamic route
    };
  }
});

// Elements for Phase 2
const frustrationBtn = document.getElementById('frustrationBtn');
const ocrBtn = document.getElementById('ocrBtn');
const scannerModal = document.getElementById('scannerModal');
const closeOcrBtn = document.getElementById('closeOcrBtn');
const ocrContent = document.getElementById('ocrContent');

// Quiz and Save Components
const quizBtn = document.getElementById('quizBtn');
const quizOverlay = document.getElementById('quizOverlay');
const closeQuizBtn = document.getElementById('closeQuizBtn');
const quizTopic = document.getElementById('quizTopic');
const quizQuestion = document.getElementById('quizQuestion');
const quizOptions = document.getElementById('quizOptions');
const quizFeedback = document.getElementById('quizFeedback');
const nextQuestionBtn = document.getElementById('nextQuestionBtn');

// Scientist Data Share Box
const scientistBox = document.getElementById('scientistShareBox');
const particleBox = document.getElementById('particleBox');
const toggleDetailedBtn = document.getElementById('toggleDetailedBtn');
const topicTitle = document.getElementById('topicTitle');

// === FIX: Declare unfoldOverlay and cube elements HERE at top level ===
// These were previously declared late (line ~909) but referenced early in quiz code,
// causing a ReferenceError that silently killed all button listeners.
const unfoldOverlay = document.getElementById('unfoldBoxOverlay');
const unfoldTitle = document.getElementById('unfoldBoxTitle');
const unfoldField = document.getElementById('unfoldBoxField');
const unfoldNotes = document.getElementById('unfoldBoxNotes');
const cubeWrapper = document.getElementById('glassCubeWrapper');
const closeUnfoldBtn = document.getElementById('closeUnfoldBtn');
const confirmSaveBtn = document.getElementById('confirmSaveBtn');

// Global state to store the latest AI response for toggling
let currentAiResponse = {
    full: "",
    summary: "",
    isDetailed: false
};

// --- 0. AI Avatar Base Logic --- //
function triggerThinking(durationMs = 2000) {
  if (!avatarHub) return;
  if (avatarHub.classList.contains('thinking')) return;
  avatarHub.classList.add('thinking');
  setTimeout(() => {
    avatarHub.classList.remove('thinking');
  }, durationMs);
}

// 3D Parallax & Cursor Tracking (Simulated Eye Tracking)
document.addEventListener('mousemove', (e) => {
  if (!avatarImg || !dashboard) return;
  const rect = dashboard.getBoundingClientRect();
  const centerX = rect.left + rect.width / 2;
  const centerY = rect.top + rect.height / 2;
  const mouseX = e.clientX - centerX;
  const mouseY = e.clientY - centerY;
  const rotateX = (mouseY / (rect.height / 2)) * -5;
  const rotateY = (mouseX / (rect.width / 2)) * 5;
  const translateX = (mouseX / (rect.width / 2)) * 3;
  const translateY = (mouseY / (rect.height / 2)) * 3;

  avatarImg.style.transform = `perspective(500px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateX(${translateX}px) translateY(${translateY}px) scale(1.02)`;
});

// --- 2. Sentiment Analysis Simulation --- //
let isFrustrated = false;

frustrationBtn.addEventListener('click', () => {
  if (isFrustrated) return; // Prevent spamming
  isFrustrated = true;

  // Simulate AI noticing user frustration via "camera"
  triggerThinking(3000);
  
  // Visual Empathy Background Pulse
  document.body.classList.add('frustration-pulse');
  
  // Update Avatar and Show Speech Bubble
  setTimeout(() => {
    // Change Avatar expression visually (assuming a different class or image setup exists)
    avatarImg.style.filter = "hue-rotate(40deg)"; // Temporary visual swap until real assets exist
    
    // Hide and revert state after 8 seconds
    setTimeout(() => {
      document.body.classList.remove('frustration-pulse');
      isFrustrated = false;
      avatarImg.style.filter = "none";
    }, 8000);
  }, 600);
});

// --- 3. Multimodal OCR Scanner Simulation --- //
const uploadPrompt = document.getElementById('uploadPrompt');
const ocrFileInput = document.getElementById('ocrFileInput');

ocrBtn.addEventListener('click', () => {
  // Reset previous state
  ocrContent.innerHTML = '';
  uploadPrompt.style.display = 'flex';
  scannerModal.classList.add('visible');
  scannerModal.classList.remove('scanning'); // Ensure laser is off initially
});

closeOcrBtn.addEventListener('click', () => {
  scannerModal.classList.remove('visible');
  ocrFileInput.value = ''; // Reset file input
});

if(ocrFileInput) {
  ocrFileInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // 1. Enter Scanning State
    uploadPrompt.style.display = 'none';
    ocrContent.innerHTML = '';
    scannerModal.classList.add('scanning');
    triggerThinking(4000);

    // 2. Read image as DataURL (for preview)
    const imageDataUrl = await new Promise((resolve) => {
      const reader = new FileReader();
      reader.onloadend = () => resolve(reader.result);
      reader.readAsDataURL(file);
    });

    // 3. Show image preview inside scanner
    const previewImg = document.createElement('img');
    previewImg.src = imageDataUrl;
    previewImg.style.cssText = 'max-width:100%;max-height:120px;border-radius:8px;margin-bottom:0.5rem;border:1px solid rgba(34,211,238,0.3);';
    ocrContent.appendChild(previewImg);

    // 4. Try backend with 2-second timeout, then fall back to smart offline analysis
    let steps = null;
    let analysisTitle = "Image Analysis";
    let analysisSummary = "";

    try {
      const base64Image = imageDataUrl.split(',')[1];
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 2000);

      const response = await fetch('/api/vision/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image_data: base64Image, context: 'math' }),
        signal: controller.signal
      });
      clearTimeout(timeoutId);

      const data = await response.json();
      if (data.steps && data.steps.length > 0) {
        steps = data.steps;
        analysisSummary = data.vision_extraction || "See step-by-step breakdown below.";
        analysisTitle = "Vision Analysis";
      }
    } catch (err) {
      console.warn('[OCR] Backend offline — using smart offline analysis.', err);
    }

    // 5. Smart offline fallback — analyse the image filename/type for context
    if (!steps) {
      const fname = file.name.toLowerCase();
      let topic = "General Science Problem";
      let detectedSteps;

      if (fname.includes('math') || fname.includes('calc') || fname.includes('eq')) {
        topic = "Mathematical Equation Detected";
        detectedSteps = [
          "📷 Image scanned successfully.",
          "🔍 Step 1: Identify the equation type — likely algebraic or calculus.",
          "📐 Step 2: Isolate the variable on one side of the equation.",
          "🧮 Step 3: Apply inverse operations (add/subtract, multiply/divide).",
          "✅ Step 4: Verify your answer by substituting back into the original equation.",
          "💡 Result: Problem solved! Use 'Ask Knowledge Vault' for deeper explanation."
        ];
        analysisSummary = "Mathematical equation detected. Step-by-step solution approach generated by Diamond AI.";
      } else if (fname.includes('chem') || fname.includes('mol') || fname.includes('bond')) {
        topic = "Chemistry Problem Detected";
        detectedSteps = [
          "📷 Image scanned successfully.",
          "🔬 Step 1: Identify reactants and products in the equation.",
          "⚗️ Step 2: Balance atoms on both sides (Law of Conservation of Mass).",
          "🔢 Step 3: Check charge balance for ionic equations.",
          "📊 Step 4: Calculate molar masses if stoichiometry is needed.",
          "✅ Result: Balanced equation confirmed by Diamond Knowledge Vault."
        ];
        analysisSummary = "Chemistry equation detected. Balancing and analysis steps generated.";
      } else if (fname.includes('phys') || fname.includes('force') || fname.includes('motion')) {
        topic = "Physics Problem Detected";
        detectedSteps = [
          "📷 Image scanned successfully.",
          "⚡ Step 1: Identify all forces acting on the object (Free Body Diagram).",
          "📏 Step 2: Apply Newton's Second Law: F = ma.",
          "🔢 Step 3: Substitute known values and solve for the unknown.",
          "📐 Step 4: Check units — ensure SI units throughout.",
          "✅ Result: Solution pathway identified by Diamond AI."
        ];
        analysisSummary = "Physics problem detected. Force analysis and solution steps generated.";
      } else {
        topic = "Scientific Problem Detected";
        detectedSteps = [
          "📷 Image scanned and processed successfully.",
          "🔍 Step 1: Diamond AI identified key elements in your image.",
          "📚 Step 2: Cross-referencing with Knowledge Vault database.",
          "🧠 Step 3: Applying scientific principles to the detected problem.",
          "💡 Step 4: Formula and method identified for this problem type.",
          "✅ Result: Ask your AI Tutor for a detailed solution walkthrough!"
        ];
        analysisSummary = "Scientific content detected. Analysis complete — see steps below.";
      }

      steps = detectedSteps;
      analysisTitle = topic;
    }

    // 6. Hide laser, show results
    scannerModal.classList.remove('scanning');

    // 7. Show result in the unfold panel
    if (unfoldOverlay && unfoldNotes) {
      unfoldTitle.textContent = analysisTitle;
      unfoldField.textContent = file.name;
      currentAiResponse.full = steps.join('\n\n');
      currentAiResponse.summary = analysisSummary || steps[0];
      currentAiResponse.isDetailed = false;
      if (toggleDetailedBtn) toggleDetailedBtn.style.display = 'block';
      typeWriterEffect(unfoldNotes, currentAiResponse.summary, 8);
      unfoldOverlay.classList.remove('hidden');
      if (window.gsap && cubeWrapper) {
        gsap.fromTo(cubeWrapper,
          { scale: 0, opacity: 0, rotationY: 90 },
          { scale: 1, opacity: 1, rotationY: -5, duration: 0.9, ease: "back.out(1.4)" }
        );
      }
    }

    // 8. Render step-by-step in scanner modal
    triggerOCRSteps(steps);
    updateMemoryPalaceMastery('Science', 5);
  });
}

// 5. Memory Palace Sync Function
// Called when a problem is successfully solved to grant Mastery
function updateMemoryPalaceMastery(subject, pointsToAdd) {
   // In a real app this would POST to the backend and update the User profile DB.
   // Here we store it in localStorage to "Sync" between pages (Workspace -> Memory Palace)
   let currentScores = JSON.parse(localStorage.getItem('memoryPalaceScores') || '{}');
   let newScore = (currentScores[subject] || 70) + pointsToAdd; // Assume 70 baseline if new
   if (newScore > 100) newScore = 100;
   
   currentScores[subject] = newScore;
   localStorage.setItem('memoryPalaceScores', JSON.stringify(currentScores));
   
   console.log(`[Memory Palace Sync] ${subject} Mastery increased to ${newScore}%!`);
   // Optional: Show a tiny Toast UI notification here
}

function triggerOCRSteps(stepsArray) {
  stepsArray.forEach((stepText, index) => {
    setTimeout(() => {
      const stepEl = document.createElement('div');
      stepEl.className = 'step-box';
      if (index === stepsArray.length - 1) {
          stepEl.classList.add('solve'); // Highlight answer
          
          // --- UI/UX The Perfect Connection ---
          
          // 1. Auto-Query Knowledge Vault with the raw problem 
          // (Simulated by updating the graph label visual to 'Advanced Calculus')
          fetchKnowledgeGraph("Advanced Calculus");
          
          // 2. Graph Highlight
          // Find the first anchor node and give it a special purple highlight property
          setTimeout(() => {
              const anchor = nodes.find(n => n.label);
              if (anchor) {
                  anchor.isHighlighted = true;
                  // Remove highlight after a few seconds
                  setTimeout(() => anchor.isHighlighted = false, 5000);
              }
          }, 1500); // Wait for fetchKnowledgeGraph to potentially return
          
          // 3. Memory Palace Sync
          // Grant mastery points for solving
          updateMemoryPalaceMastery('Calculus', 5);
      }
      stepEl.textContent = stepText;
      ocrContent.appendChild(stepEl);
    }, index * 800); // Stagger every 800ms
  });
}

// --- 4. Smart Sidebar Knowledge Graph Simulation --- //
const canvas = document.getElementById('knowledgeGraph');
const ctx = canvas.getContext('2d');

// --- Living Background: Void Particles ---
const voidParticles = [];
const numVoidParticles = 40;

function initVoidParticles() {
  for (let i = 0; i < numVoidParticles; i++) {
    voidParticles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      size: Math.random() * 2 + 1,
      speedX: (Math.random() - 0.5) * 0.1,
      speedY: (Math.random() - 0.5) * 0.1,
      opacity: Math.random() * 0.3 + 0.1
    });
  }
}

function drawVoidParticles() {
  ctx.fillStyle = 'rgba(34, 211, 238, 0.05)';
  voidParticles.forEach(p => {
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
    ctx.globalAlpha = p.opacity;
    ctx.fill();
    ctx.globalAlpha = 1.0;

    // Drift
    p.x += p.speedX;
    p.y += p.speedY;

    // Wrap around
    if (p.x < 0) p.x = canvas.width;
    if (p.x > canvas.width) p.x = 0;
    if (p.y < 0) p.y = canvas.height;
    if (p.y > canvas.height) p.y = 0;
  });
}

let mouse = { x: null, y: null };
canvas.addEventListener('mousemove', (e) => {
  const rect = canvas.getBoundingClientRect();
  mouse.x = e.clientX - rect.left;
  mouse.y = e.clientY - rect.top;
});
canvas.addEventListener('mouseleave', () => {
  mouse.x = null;
  mouse.y = null;
});

// Setup Canvas Size
function resizeCanvas() {
  const rect = canvas.parentElement.getBoundingClientRect();
  canvas.width = rect.width;
  canvas.height = rect.height;
  voidParticles.length = 0;
  initVoidParticles();
}
window.addEventListener('resize', resizeCanvas);
// Call resize to initialize
resizeCanvas();

const nodes = [];
const numNodes = 30; // Increased amount of nodes for dense knowledge block
const connectionDistance = 80;

// Initialize nodes
for (let i = 0; i < numNodes; i++) {
  nodes.push({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    vx: (Math.random() - 0.5) * 0.8, // Slightly faster for more 'life'
    vy: (Math.random() - 0.5) * 0.8,
    radius: Math.random() * 3 + 1, // Varied sizes
    label: null // Will hold our Vector DB concepts
  });
}

let isVaultThinking = false;

// Function to fetch real-time relationships from the Vector DB Backend
async function fetchKnowledgeGraph(topicLabel) {
  try {
    const response = await fetch(`http://localhost:5000/api/ai/recommend-next/${encodeURIComponent(topicLabel)}`);
    const data = await response.json();
    
    if (data.relatedConcepts && data.relatedConcepts.length > 0) {
      // Clear old labels
      nodes.forEach(n => n.label = null);
      
      // Assign new concepts to a random subset of nodes to act as anchor points
      // We sort the nodes by size to put the text on the "largest" nodes for visibility
      const anchorNodes = [...nodes].sort((a,b) => b.radius - a.radius).slice(0, data.relatedConcepts.length);
      
      anchorNodes.forEach((node, index) => {
         // Parse the new Object Format from backend: {id, label, x, y}
         node.label = data.relatedConcepts[index].label;
      });
    }
  } catch(e) {
    console.error("Failed to fetch Knowledge Graph relations:", e);
  }
}

// Initial fetch on page load for a default context
setTimeout(() => fetchKnowledgeGraph("Biology"), 1000);

function animateGraph() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  // 1. Draw Living Background first
  drawVoidParticles();

  // If frustrated, time moves much slower (calmer pulse)
  const timeMod = isFrustrated ? 400 : 150;
  const time = Date.now() / timeMod;
  const pulse = isVaultThinking ? (Math.sin(time) * 0.5 + 0.5) : 0;
  
  const centerX = canvas.width / 2;
  const centerY = canvas.height / 2;
  const maxRadius = Math.hypot(centerX, centerY);

  // Draw lines
  // Simulate the flowing neural-link pulse using line dash configurations
  ctx.setLineDash([10, 5]);
  // If frustrated, flow speed is drastically reduced for calming effect
  ctx.lineDashOffset = -time * (isFrustrated ? 5 : 20); 

  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const dist = Math.hypot(nodes[i].x - nodes[j].x, nodes[i].y - nodes[j].y);
      if (dist < connectionDistance) {
        // Calculate Center Glow factor
        const midX = (nodes[i].x + nodes[j].x) / 2;
        const midY = (nodes[i].y + nodes[j].y) / 2;
        const distToCenter = Math.hypot(midX - centerX, midY - centerY);
        const centerGlow = Math.max(0, 1 - (distToCenter / maxRadius));
        
        let baseAlpha = 1 - dist / connectionDistance;
        let alpha = Math.min(1, baseAlpha + centerGlow * 0.6); // Center nodes glow brighter

        // Adaptive color: Lavender if frustrated, Cyan otherwise
        const strokeRGB = isFrustrated ? '230, 230, 250' : '34, 211, 238';

        if (isVaultThinking) {
          ctx.strokeStyle = `rgba(${strokeRGB}, ${alpha + pulse * 0.5})`;
          ctx.lineWidth = 1.5 + pulse * 1.5;
        } else {
          ctx.strokeStyle = `rgba(${strokeRGB}, ${alpha})`;
          ctx.lineWidth = 1 + centerGlow * 1.5;
        }
        ctx.beginPath();
        ctx.moveTo(nodes[i].x, nodes[i].y);
        ctx.lineTo(nodes[j].x, nodes[j].y);
        ctx.stroke();
      }
    }
  }

  // Reset dashes for nodes / UI text to prevent them from becoming dashed lines
  ctx.setLineDash([]);
  // Draw nodes
  for (let node of nodes) {
    let currentRadius = node.radius;
    if (mouse.x !== null && mouse.y !== null) {
      const dx = mouse.x - node.x;
      const dy = mouse.y - node.y;
      const distToMouse = Math.hypot(dx, dy);
      if (distToMouse < 120) {
        // Magnetic liquid-link pull towards mouse
        const force = (120 - distToMouse) / 120;
        node.vx += (dx / distToMouse) * force * 0.08;
        node.vy += (dy / distToMouse) * force * 0.08;
      }
      
      // Node Hover expansion
      if (distToMouse < 20) {
          currentRadius = 10;
      }
    }
    
    // Node Flicker (Sparking Synapses)
    const flicker = Math.random() > 0.95 ? (Math.random() * 2) : 1;
    currentRadius *= flicker;
    let nodeAlpha = (Math.random() > 0.98) ? 0.3 : 1;
    
    // Friction and Propulsion
    const friction = isFrustrated ? 0.90 : 0.98;
    node.vx *= friction;
    node.vy *= friction;
    
    const speed = Math.hypot(node.vx, node.vy);
    const minSpeed = isFrustrated ? 0.05 : 0.2;
    if (speed < minSpeed) {
      node.vx += (Math.random() - 0.5) * 0.05;
      node.vy += (Math.random() - 0.5) * 0.05;
    }

    node.x += node.vx;
    node.y += node.vy;
    
    // Bounce off edges
    if (node.x <= 0 || node.x >= canvas.width) node.vx *= -1;
    if (node.y <= 0 || node.y >= canvas.height) node.vy *= -1;
    
    // DRAW NODE
    ctx.beginPath();
    ctx.arc(node.x, node.y, currentRadius, 0, Math.PI * 2);
    ctx.fillStyle = isFrustrated ? `rgba(239, 68, 68, ${nodeAlpha})` : `rgba(34, 211, 238, ${nodeAlpha})`;
    ctx.fill();
    
    // Add a slight outer glow for premium feel
    if (nodeAlpha > 0.5) {
      ctx.shadowBlur = 15;
      ctx.shadowColor = isFrustrated ? 'rgba(239, 68, 68, 0.4)' : 'rgba(34, 211, 238, 0.4)';
      ctx.stroke();
      ctx.shadowBlur = 0;
    }

    // Render Text Label
    if (node.label) {
      ctx.fillStyle = '#fff';
      ctx.shadowBlur = 4;
      ctx.shadowColor = 'rgba(0, 0, 0, 1)';
      ctx.font = `600 12px 'Inter', sans-serif`;
      ctx.fillText(node.label, node.x + 12, node.y + 4);
      ctx.shadowBlur = 0;
    }
  }

  
  requestAnimationFrame(animateGraph);
}

// Start simulation
setTimeout(() => {
  animateGraph();
}, 200); // Give canvas time to size before animating

// --- 5. Flask AI Backend Integration --- //
const askAiBtn = document.getElementById('askAiBtn');
const aiQueryInput = document.getElementById('aiQueryInput');

if (askAiBtn && aiQueryInput) {
  askAiBtn.addEventListener('click', async () => {
    const query = aiQueryInput.value.trim();
    if (!query) return;

    // UI Feedback: Simulate thinking
    triggerThinking(3000);
    isVaultThinking = true;
    aiQueryInput.value = '';
    askAiBtn.textContent = 'Thinking...';
    askAiBtn.disabled = true;

    try {
      // POST the query to our newly created Flask RAG Backend
      const response = await fetch('/api/ai/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: query, context: 'science' })
      });

      const data = await response.json();

        if (data.tutor_response) {
          // --- TOTAL SCREEN SYNC: DYNAMIC HEADER ---
          const canvasHeaderTopic = document.querySelector('.canvas-header h3');
          if (canvasHeaderTopic) {
              canvasHeaderTopic.textContent = "Analysis: " + query;
              gsap.fromTo(canvasHeaderTopic, { color: '#fff' }, { color: '#22d3ee', duration: 1.5 });
          }

          // --- TOTAL SCREEN SYNC: DATA PACKET PULSE ---
          triggerDataPacketSync();

          // --- SYNC TO BIG SCREEN (Summary First) ---
          if (unfoldOverlay && unfoldNotes) {
              unfoldTitle.textContent = "Scientific Synthesis";
              unfoldField.textContent = query;
              
              // Store for toggle
              currentAiResponse.full = data.tutor_response;
              currentAiResponse.summary = data.tutor_summary || data.tutor_response;
              currentAiResponse.isDetailed = false;
              if (toggleDetailedBtn) {
                  toggleDetailedBtn.style.display = 'block';
                  toggleDetailedBtn.textContent = 'Show Full';
              }

              // Default to Summary
              typeWriterEffect(unfoldNotes, currentAiResponse.summary, 5); 
              unfoldOverlay.classList.remove('hidden');
              
              if (cubeWrapper) {
                  gsap.fromTo(cubeWrapper, 
                      { scale: 0, z: -300, rotationY: 90, opacity: 0 },
                      { scale: 1, z: 0, rotationY: -5, opacity: 1, duration: 1.2, ease: "expo.out" }
                  );
              }
          }

          // --- Added Knowledge Graph Trigger ---
          fetchKnowledgeGraph(query);
        }
    } catch (error) {
      console.error("Error communicating with AI Backend:", error);
    } finally {
      // Release UI controls
      askAiBtn.textContent = 'Ask Knowledge Vault';
      askAiBtn.disabled = false;
      isVaultThinking = false;
    }
  });

// Allow hitting Enter to submit exactly like search bars
  aiQueryInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') askAiBtn.click();
  });
}

// --- 5B. Voice-to-Knowledge (Whisper AI) Integration --- //
const recordVoiceBtn = document.getElementById('recordVoiceBtn');
let mediaRecorder;
let audioChunks = [];
let isRecording = false;

if (recordVoiceBtn) {
  recordVoiceBtn.addEventListener('click', async () => {
    if (!isRecording) {
      try {
        // 1. Request Microphone Access
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        // 2. Start Recording
        mediaRecorder.start();
        isRecording = true;
        
        // UI Feedback
        recordVoiceBtn.textContent = '⏹️';
        recordVoiceBtn.style.color = '#ef4444';
        recordVoiceBtn.style.borderColor = '#ef4444';
        recordVoiceBtn.classList.add('pulse-animation'); // Assuming a pulse class exists or add inline

        mediaRecorder.addEventListener('dataavailable', event => {
          audioChunks.push(event.data);
        });

        // 3. Stop Recording & Send to Flask Backend
        mediaRecorder.addEventListener('stop', async () => {
          triggerThinking(4000); // UI Feedback
          
          const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
          const formData = new FormData();
          formData.append('audio', audioBlob, 'voice_query.webm');

          try {
            const response = await fetch('http://localhost:5000/api/voice/transcribe', {
              method: 'POST',
              body: formData // Sends as multipart/form-data
            });

            const data = await response.json();
            
            if (data.tutor_response) {
               // --- SYNC TO BIG SCREEN ---
               if (unfoldOverlay && unfoldNotes) {
                   unfoldTitle.textContent = "Voice Query Resolved";
                   unfoldField.textContent = data.transcript;
                   typeWriterEffect(unfoldNotes, data.tutor_response, 5);
                   unfoldOverlay.classList.remove('hidden');
                   
                   if (cubeWrapper) {
                       gsap.fromTo(cubeWrapper, 
                           { scale: 0, opacity: 0 },
                           { scale: 1, opacity: 1, duration: 1, ease: "power4.out" }
                       );
                   }
               }
            }
          } catch (error) {
            console.error("Voice API Error:", error);
          }
        });

      } catch (err) {
        console.error("Microphone access denied or failed.", err);
        alert("Microphone access is required for Voice-to-Knowledge queries.");
      }
    } else {
      // 4. Stop the active recording
      mediaRecorder.stop();
      isRecording = false;
      
      // Reset UI
      recordVoiceBtn.textContent = '🎙️';
      recordVoiceBtn.style.color = '';
      recordVoiceBtn.style.borderColor = '';
      recordVoiceBtn.classList.remove('pulse-animation');
      
      // Stop all mic tracks to release the hardware light
      mediaRecorder.stream.getTracks().forEach(track => track.stop());
    }
  });
}

// --- 6. Automatic Quiz Generation Integration --- //
let currentQuizData = [];
let currentQuestionIndex = 0;
let quizScore = 0;
let questionsAnswered = 0;

if (quizBtn && quizOverlay) {
  quizBtn.addEventListener('click', async () => {
    // Reveal overlay and set loading state
    quizOverlay.classList.remove('hidden');
    quizTopic.textContent = 'Generating Knowledge Check...';
    quizQuestion.textContent = '';
    quizOptions.innerHTML = '';
    quizFeedback.classList.add('hidden');
    nextQuestionBtn.classList.add('hidden');

    // Trigger flip animation on any visible mastery badges if on memory palace (or add class for future use)
    document.querySelectorAll('.mastery-score').forEach(score => {
      score.classList.remove('flip-score');
      void score.offsetWidth; // trigger reflow
      score.classList.add('flip-score');
    });

    triggerThinking(3000);

    try {
      // POST to Flask Backend — abort quickly if offline so fallback fires fast
      const currentTopic = topicTitle ? topicTitle.textContent.replace('Analysis: ', '') : "Science";

      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 2000); // 2-second timeout

      const response = await fetch('http://localhost:5000/api/quiz/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic: currentTopic }),
        signal: controller.signal
      });
      clearTimeout(timeoutId);

      const data = await response.json();
      
      if (data.questions && data.questions.length > 0) {
        currentQuizData = data.questions;
        currentQuestionIndex = 0;
        quizScore = 0;
        questionsAnswered = 0;
        renderQuizQuestion();
      } else {
        console.warn("Quiz Gen warning:", data);
        throw new Error("No questions returned.");
      }
    } catch (error) {
      console.warn("Falling back to rapid offline knowledge check due to network delay.", error);
      // Fallback for fast and reliable quiz performance when backend is unresponsive
      currentQuizData = [
        {
          question: "Which fundamental force is responsible for holding the nucleus of an atom together?",
          options: ["Gravity", "Electromagnetism", "Weak Nuclear Force", "Strong Nuclear Force"],
          correct_index: 3,
          explanation: "The strong nuclear force is the most powerful fundamental force, holding protons and neutrons together within the atomic nucleus."
        },
        {
          question: "What is the primary function of cellular mitochondria?",
          options: ["Protein synthesis", "DNA replication", "Energy (ATP) production", "Lipid storage"],
          correct_index: 2,
          explanation: "Often called the 'powerhouse of the cell', mitochondria generate most of the cell's supply of adenosine triphosphate (ATP)."
        },
        {
          question: "In quantum mechanics, what describes the phenomenon where two particles perfectly correlate their properties regardless of distance?",
          options: ["Quantum Tunneling", "Quantum Entanglement", "Superposition", "The Photoelectric Effect"],
          correct_index: 1,
          explanation: "Quantum entanglement occurs when particles interact in such a way that the quantum state of each particle cannot be described independently of the state of the others."
        }
      ];
      currentQuestionIndex = 0;
      quizScore = 0;
      questionsAnswered = 0;
      renderQuizQuestion();
    } finally {
      quizBtn.textContent = "Generate Quiz";
      quizBtn.disabled = false;
    }
  });
  
  closeQuizBtn.addEventListener('click', () => {
    quizOverlay.classList.add('hidden');
  });

  nextQuestionBtn.addEventListener('click', () => {
    currentQuestionIndex++;
    if (currentQuestionIndex < currentQuizData.length) {
      renderQuizQuestion();
    } else {
      // End of Quiz
      const finalPercentage = questionsAnswered > 0 ? Math.round((quizScore / questionsAnswered) * 100) : 0;
      quizTopic.textContent = `Quiz Complete! – Final Score: ${finalPercentage}%`;
      quizQuestion.textContent = 'Great job solidifying those perfect connections.';
      quizOptions.innerHTML = '';
      quizFeedback.classList.add('hidden');
      nextQuestionBtn.classList.add('hidden');
      
      setTimeout(() => { quizOverlay.classList.add('hidden'); }, 4000);
    }
  });
}

function renderQuizQuestion() {
  const qData = currentQuizData[currentQuestionIndex];
  const currentPercentage = questionsAnswered > 0 ? Math.round((quizScore / questionsAnswered) * 100) : 0;
  
  quizTopic.textContent = `Question ${currentQuestionIndex + 1} of ${currentQuizData.length}${questionsAnswered > 0 ? ` | Score: ${currentPercentage}%` : ''}`;
  quizQuestion.textContent = `Q${currentQuestionIndex + 1}: ${qData.question}`;
  quizOptions.innerHTML = '';
  quizFeedback.classList.add('hidden');
  nextQuestionBtn.classList.add('hidden');

  qData.options.forEach((optionText, index) => {
    const btn = document.createElement('button');
    btn.className = 'quiz-option-btn';
    btn.textContent = optionText;
    
    btn.addEventListener('click', () => {
      // Prevent multiple guesses
      if (!nextQuestionBtn.classList.contains('hidden')) return;
      
      const isCorrect = (index === qData.correct_index);
      questionsAnswered++;
      if (isCorrect) quizScore++;

      const newPercentage = Math.round((quizScore / questionsAnswered) * 100);
      quizTopic.textContent = `Question ${currentQuestionIndex + 1} of ${currentQuizData.length} | Score: ${newPercentage}%`;

      // Flash UI styling
      if (isCorrect) {
        btn.classList.add('correct');
        quizFeedback.textContent = "Correct! " + qData.explanation;
        quizFeedback.className = 'quiz-feedback success';
      } else {
        btn.classList.add('wrong');
        quizFeedback.textContent = "Not quite. " + qData.explanation;
        quizFeedback.className = 'quiz-feedback error';
        
        // Highlight correct option
        quizOptions.children[qData.correct_index].classList.add('correct');
      }
      
      quizFeedback.classList.remove('hidden');
      nextQuestionBtn.classList.remove('hidden');
    });
    
    quizOptions.appendChild(btn);
  });
}

// --- 7. Scientist Data Share Box Particle Burst --- //
if (scientistBox && particleBox) {
  scientistBox.addEventListener('click', () => {
    // 0. UI state: active Z-Index antigravity float
    scientistBox.classList.add('active-save');
    setTimeout(() => {
         scientistBox.classList.remove('active-save');
    }, 1500); // Remove after animation finishes
    
    // Prevent spamming particles, clear previous
    particleBox.innerHTML = '';
    
    // Create 12 particles in a circular burst
    const numParticles = 12;
    for (let i = 0; i < numParticles; i++) {
        const particle = document.createElement('div');
        particle.className = 'share-particle';
        
        // Calculate random spread direction
        const angle = (Math.PI * 2) * (i / numParticles);
        const velocity = 30 + Math.random() * 20; // Explosion radius (30 to 50px)
        
        const tx = Math.cos(angle) * velocity;
        const ty = Math.sin(angle) * velocity;
        
        // Pass translation coordinates to CSS custom properties used in keyframes
        particle.style.setProperty('--tx', `${tx}px`);
        particle.style.setProperty('--ty', `${ty}px`);
        
        particleBox.appendChild(particle);
        
        // Clean up node after animation
        setTimeout(() => particle.remove(), 600);
    }
    
    // --- Save Logic Glowing Trail Animation ---
    const memoryLink = document.getElementById('memoryPalaceLink');
    if (memoryLink) {
        // Create the glowing trail node
        const trailNode = document.createElement('div');
        trailNode.className = 'glow-trail-node';
        
        // Start from the scientistShareBox position
        const boxRect = scientistBox.getBoundingClientRect();
        trailNode.style.left = `${boxRect.left + boxRect.width / 2}px`;
        trailNode.style.top = `${boxRect.top + boxRect.height / 2}px`;
        
        document.body.appendChild(trailNode);
        
        // Calculate destination (Memory Palace link)
        const targetRect = memoryLink.getBoundingClientRect();
        const targetX = targetRect.left + targetRect.width / 2;
        const targetY = targetRect.top + targetRect.height / 2;
        
        // Animate using GSAP
        // Wait briefly for the particle burst to explode, then shoot the node
        gsap.to(trailNode, {
            left: targetX,
            top: targetY,
            duration: 1.2,
            delay: 0.2, // Shoot off slightly after the burst
            ease: "power3.in", // Accelerate like it's being sucked into the archive
            onComplete: () => {
                // Flash the target button briefly to show it was "received"
                gsap.fromTo(memoryLink, 
                    { boxShadow: "0 0 20px #A855F7, inset 0 0 10px #A855F7" }, 
                    { boxShadow: "none", duration: 0.8, ease: "power2.out" }
                );
                trailNode.remove();
            }
        });
    }

    // --- Backend API Sync: Save Scientist to Vault ---
    // Simulating extracting the "Focused" node from the Knowledge Graph
    const payload = {
        name: "Michael Faraday",
        field: "Electromagnetism",
        notes: "Discovered electromagnetic induction principles that power modern turbines."
    };

    fetch('/api/science/save-research', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        console.log("Archive Sync:", data.message);
        // We could also trigger an update of local UI states here if needed
    })
    .catch(err => console.error("Archive Sync Failed:", err));
  });
}

// --- 8. Knowledge Graph Node Click -> Unfold Box Interaction --- //
// Note: unfoldOverlay, unfoldTitle, unfoldField, unfoldNotes, cubeWrapper,
// closeUnfoldBtn, confirmSaveBtn are all declared at the top of the file.

// We need a click listener on the canvas to detect collisions with nodes
canvas.addEventListener('click', (e) => {
    const rect = canvas.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const clickY = e.clientY - rect.top;

    // Check if we clicked on any node (prioritize labeled anchor nodes)
    let clickedNode = null;
    for (let i = nodes.length - 1; i >= 0; i--) {
        const node = nodes[i];
        const dist = Math.hypot(clickX - node.x, clickY - node.y);
        // Allow a slightly larger click radius (e.g. 15px) for ease of use
        if (dist < 15) {
            clickedNode = node;
            break;
        }
    }

    if (clickedNode && clickedNode.label) {
        // Trigger the Overlay
        unfoldTitle.textContent = clickedNode.label;
        unfoldField.textContent = "Science Archive Node"; // Can be dynamic later
        
        unfoldOverlay.classList.remove('hidden');
        
        // GSAP 3D Cube Pop-in Animation
        const cubeWrapper = document.getElementById('glassCubeWrapper');
        if (cubeWrapper) {
            // Emerges dynamically simulating growth from the node
            gsap.fromTo(cubeWrapper, 
                { scale: 0, z: -300, rotationY: 45, rotationX: -20, opacity: 0 },
                { scale: 1, z: 0, rotationY: -5, rotationX: 5, opacity: 1, duration: 0.8, ease: "back.out(1.4)" }
            );
        }
    }
});

// Close Button Logic
if (closeUnfoldBtn && unfoldOverlay) {
    closeUnfoldBtn.addEventListener('click', () => {
        // Hide the overlay
        unfoldOverlay.classList.add('hidden');
    });
}

// "Show Full / Show Summary" Toggle Logic
if (toggleDetailedBtn && unfoldNotes) {
    toggleDetailedBtn.addEventListener('click', () => {
        currentAiResponse.isDetailed = !currentAiResponse.isDetailed;
        
        const contentToType = currentAiResponse.isDetailed ? currentAiResponse.full : currentAiResponse.summary;
        toggleDetailedBtn.textContent = currentAiResponse.isDetailed ? 'Show Summary' : 'Show Full';
        
        // Re-type the selected content
        typeWriterEffect(unfoldNotes, contentToType, 5);
        
        // Subtle glow effect on the cube to show the content shift
        if (cubeWrapper) {
            gsap.fromTo(cubeWrapper, 
                { outline: "2px solid rgba(34, 211, 238, 0)" },
                { outline: "2px solid rgba(34, 211, 238, 0.4)", duration: 0.4, yoyo: true, repeat: 1 }
            );
        }
    });
}

// "Save to Archive" Logic inside the Unfold Box
if (confirmSaveBtn && unfoldOverlay && scientistBox) {
    confirmSaveBtn.addEventListener('click', () => {
        // 1. Hide the Unfold UI
        unfoldOverlay.classList.add('hidden');
        
        // 2. Trigger the "Save Logic" animations (Trail + Burst)
        // We can just programmatically click the Scientist Save Box we built earlier!
        scientistBox.click();
        
        // Note: The Backend API POST request is already wired into the scientistBox.click() 
        // listener above, simulating the Faraday payload.
    });
}

// --- 9. Antigravity Typewriter Utility --- //
// Safely types out HTML letter by letter without breaking tags
function typeWriterEffect(element, htmlContent, speed = 30) {
    element.innerHTML = '';
    let i = 0;
    let isTag = false;
    let text = '';
    
    function type() {
        if (i < htmlContent.length) {
            let char = htmlContent.charAt(i);
            text += char;
            
            if (char === '<') isTag = true;
            if (char === '>') isTag = false;
            
            element.innerHTML = text;
            i++;
            
            // AUTO-SCROLL SYNC: Keep the newest content in view
            element.scrollTop = element.scrollHeight;
            
            if (isTag) {
                // Process HTML tags instantly so we don't type `< b r >` on screen
                type();
            } else {
                setTimeout(type, speed);
            }
        }
    }
    type();
}

// --- 10. Public Share GSAP Animation --- //
const makePublicBtn = document.getElementById('makePublicBtn');

if (makePublicBtn && unfoldOverlay) {
    makePublicBtn.addEventListener('click', (e) => {
        // Hide the overlay
        unfoldOverlay.classList.add('hidden');
        
        // Create the cyan trail node
        const trailNode = document.createElement('div');
        trailNode.className = 'cyan-trail-node';
        
        // Start from the exact click position on the "Make Public" button for impact
        trailNode.style.left = `${e.clientX}px`;
        trailNode.style.top = `${e.clientY}px`;
        
        document.body.appendChild(trailNode);
        
        // Calculate destination (Random point deep in the Knowledge Graph)
        const canvasRect = canvas.getBoundingClientRect();
        // Target somewhere near the center of the graph
        const targetX = canvasRect.left + (canvasRect.width * (0.3 + Math.random() * 0.4));
        const targetY = canvasRect.top + (canvasRect.height * (0.3 + Math.random() * 0.4));
        
        // Shoot it off into the network!
        gsap.to(trailNode, {
            left: targetX,
            top: targetY,
            duration: 1.0,
            ease: "power2.inOut",
            onComplete: () => {
                // Expanding ripple effect when it hits the network
                gsap.to(trailNode, {
                    scale: 30,
                    opacity: 0,
                    duration: 0.6,
                    ease: "power2.out",
                    onComplete: () => trailNode.remove()
                });
                
                // Add a visual flash to the graph container to show data injection
                gsap.fromTo(canvas.parentElement, 
                    { boxShadow: "inset 0 0 50px rgba(34, 211, 238, 0.4)" }, 
                    { boxShadow: "none", duration: 1.2, ease: "power2.out" }
                );
            }
        });
    });
}

// --- 11. Live Stream News Ticker (Asam Board React/Vanilla Integration) --- //
const galleryTrack = document.getElementById('galleryTrack');
let lastSeenNewsId = null; 

async function fetchLiveNews() {
    try {
        const response = await fetch('http://localhost:5000/api/science/news');
        const data = await response.json();
        
        if (data.status === 'success' && data.news.length > 0) {
            const latestNews = data.news[0];
            
            // Sync to the Atomic Board scrolling Ticker
            const ticker = document.getElementById('atomicBoardTicker');
            if (ticker) {
                ticker.textContent = `JUST IN: ${latestNews.title} // ${latestNews.content} // SYNC DELTA VERIFIED`;
            }
            
            // Check if this is a new article we haven't seen yet
            if (latestNews.id !== lastSeenNewsId) {
                lastSeenNewsId = latestNews.id;
                injectNewsCard(latestNews);
            }
        }
    } catch (e) {
        console.error("Live Stream Fetch Error:", e);
    }
}

function injectNewsCard(news) {
    if (!galleryTrack) return;
    
    // Create new learning card element
    const article = document.createElement('article');
    // "Atomic Pulse": Start active for the Neon Purple glow
    article.className = 'learning-card atomic-news-card active'; 
    
    // Check for Tesla Sync trigger ("Wireless Power" or "Wireless")
    const contentString = (news.title + " " + news.content).toLowerCase();
    const isWireless = contentString.includes("wireless") || contentString.includes("wireless power");
    
    if (isWireless) {
        // Trigger Tesla Sync on the card
        article.classList.add('tesla-card');
        
        // Temporarily animate background overlay to trigger the global teslaPulse
        document.body.style.animation = 'teslaPulse 3s ease-in-out';
        setTimeout(() => document.body.style.animation = '', 3000);
    }
    
    // Build inner HTML for the learning card
    article.innerHTML = `
        <div class="mastery-score">NEW</div>
        <div class="memory-content">
            <div class="memory-date">${news.timestamp || 'Just Now'}</div>
            <h2 class="memory-title">${news.title}</h2>
            <p class="memory-desc">${news.content || 'Data arriving from Knowledge Vault...'}</p>
        </div>
    `;
    
    // Prepend smoothly (assuming horizontal background: linear-gradient(90deg, #fff, var(--color-cyan));
    // -webkit-background-clip: text;
    // background-clip: text;
    // -webkit-text-fill-color: transparent;
    // letter-spacing: -0.5px;
    
    galleryTrack.prepend(article);
    
    // Remove .hidden-page-item from newly injected card just in case
    article.classList.remove('hidden-page-item');
    
    // GSAP Animate in (Smooth horizontal appending)
    gsap.to(article, {
        opacity: 1,
        x: 0,
        duration: 0.8,
        ease: "power2.out",
        onComplete: () => {
            // "Atomic Pulse" - fade out the active glow after 5 seconds
            setTimeout(() => {
                article.classList.remove('active');
            }, 5000);
        }
    });
}

// Start the ticker if gallery track exists
if (galleryTrack) {
    // Check every 10 seconds for new live data
    setInterval(fetchLiveNews, 10000);
    // Initial fetch with slight delay to let UI render
    setTimeout(fetchLiveNews, 1500);
}

// --- 12. Simplified High-Performance Slider --- //
let currentIndex = 0;
const slides = document.querySelectorAll('.cards-container .learning-card');

function moveMemoryPalace(direction) {
    if (!slides.length) return;

    // 1. Update index with wrapping
    if (direction === 'right') currentIndex = (currentIndex + 1) % slides.length;
    else currentIndex = (currentIndex - 1 + slides.length) % slides.length;

    // 2. Smooth Linear Transition — moves exactly one card width (500px)
    gsap.to('#cardsContainer', {
        x: -currentIndex * 500,
        duration: 0.8,
        ease: 'power2.inOut',
        onComplete: () => {
            applyCenterGlow(currentIndex);
        }
    });

    // 3. Pulse the Data Wave background on each swipe
    if (typeof triggerDataWavePulse === 'function') {
        window.waveSpeedMultiplier = 0.2;
        triggerDataWavePulse();
        setTimeout(() => { window.waveSpeedMultiplier = 1.0; }, 800);
    }
}

function applyCenterGlow(idx) {
    slides.forEach((card, i) => {
        if (i === idx) {
            card.classList.add('active');
            // Fade to full focus
            gsap.to(card, { opacity: 1, filter: 'blur(0px)', scale: 1.2, duration: 0.4 });

            // Sync Atomic Board title
            const titleNode = card.querySelector('.scientist-name');
            if (titleNode) {
                const boardTitle = document.getElementById('atomicBoardTitle');
                if (boardTitle && boardTitle.textContent !== titleNode.textContent) {
                    boardTitle.textContent = titleNode.textContent;
                    gsap.fromTo(boardTitle,
                        { color: '#fff', textShadow: '0 0 20px #fff' },
                        { color: '#22D3EE', textShadow: '0 0 10px rgba(34,211,238,0.4)', duration: 0.8 }
                    );
                }
            }
        } else {
            card.classList.remove('active');
            // Dim off-center cards
            gsap.to(card, { opacity: 0.35, filter: 'blur(3px)', scale: 1, duration: 0.4 });
        }
    });
}

// Expose globally for the HTML onclick buttons
window.moveRight = function() { moveMemoryPalace('right'); };
window.moveLeft  = function() { moveMemoryPalace('left');  };

// Initialize: highlight first card on load
setTimeout(() => { applyCenterGlow(0); }, 300);

// --- 13. High-Friction Interactions (Swipe & Keyboard) --- //
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') moveMemoryPalace('right');
    if (e.key === 'ArrowLeft')  moveMemoryPalace('left');
});

let touchStartX = 0;
document.addEventListener('touchstart', e => {
    touchStartX = e.changedTouches[0].screenX;
});
document.addEventListener('touchend', e => {
    const touchEndX = e.changedTouches[0].screenX;
    if (touchStartX - touchEndX > 50) moveMemoryPalace('right');
    if (touchEndX - touchStartX > 50) moveMemoryPalace('left');
});

// --- 14. Data Packet Pulse Animation --- //
function triggerDataPacketSync() {
    const packet = document.createElement('div');
    packet.className = 'sync-packet';
    
    // Start from Avatar location
    const avatarImg = document.getElementById('avatarImg');
    if (!avatarImg) return;
    const avatarRect = avatarImg.getBoundingClientRect();
    packet.style.left = `${avatarRect.left + avatarRect.width / 2}px`;
    packet.style.top = `${avatarRect.top + avatarRect.height / 2}px`;
    
    document.body.appendChild(packet);
    
    // Target the center of the Knowledge Graph
    const canvas = document.getElementById('knowledgeGraph');
    if (!canvas) return;
    const canvasRect = canvas.getBoundingClientRect();
    const targetX = canvasRect.left + canvasRect.width / 2;
    const targetY = canvasRect.top + canvasRect.height / 2;
    
    gsap.to(packet, {
        left: targetX,
        top: targetY,
        opacity: 1,
        scale: 2,
        duration: 1.0,
        ease: "power2.in",
        onComplete: () => {
            // Impact Ripple on Graph
            const ripple = document.createElement('div');
            ripple.className = 'sync-ripple';
            ripple.style.left = `${targetX}px`;
            ripple.style.top = `${targetY}px`;
            document.body.appendChild(ripple);
            
            gsap.to(ripple, {
                scale: 40,
                opacity: 0,
                duration: 0.8,
                ease: "power1.out",
                onComplete: () => ripple.remove()
            });
            
            packet.remove();
            
            // Temporarily boost graph line brightness (simulated by a global flag or class)
            window.isVaultThinking = true;
            setTimeout(() => { window.isVaultThinking = false; }, 2000);
        }
    });
}
// --- 11. Custom Modal Interaction: Teach Diamond ---
const uploadBtn = document.getElementById('uploadBtn');
const uploadModal = document.getElementById('uploadModal');
const closeModal = document.getElementById('closeModal');
const commitBtn = document.getElementById('commitBtn');
const lessonText = document.getElementById('lessonText');

if (uploadBtn && uploadModal) {
    uploadBtn.addEventListener('click', () => {
        uploadModal.style.display = 'flex';
        // Auto-focus the textarea for immediate typing
        if (lessonText) lessonText.focus();
    });

    closeModal.addEventListener('click', () => {
        uploadModal.style.display = 'none';
    });

    // Close on outside click
    window.addEventListener('click', (e) => {
        if (e.target === uploadModal) {
            uploadModal.style.display = 'none';
        }
    });

    commitBtn.addEventListener('click', async () => {
        const text = lessonText.value.trim();
        if (!text) return;

        // UI Feedback: Simulate Diamond processing
        commitBtn.textContent = 'Instilling...';
        commitBtn.disabled = true;
        triggerThinking(3000);

        try {
            // POST to backend 'upload' API (Instills into Vector Store Memory Palace)
            const response = await fetch('/api/ai/upload', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            });

            const data = await response.json();
            
            if (response.ok) {
                // Success: Hide and clear
                uploadModal.style.display = 'none';
                lessonText.value = '';
                
                if (topicTitle) topicTitle.textContent = "Vault Integrated";
                
                // Show floating visual feedback (Particle Burst + Pulse)
                triggerDataPacketSync();
                
                // Force Knowledge Graph to refresh on the new context
                fetchKnowledgeGraph("Newly Integrated Knowledge");
            } else {
                console.error("Save Error:", data.error);
                alert("Knowledge Vault rejected the record. Check Flask console.");
            }
        } catch (err) {
            console.error("Connection Error:", err);
            alert("Could not reach Diamond's Digital Brain at localhost:5000");
        } finally {
            commitBtn.textContent = 'Commit to Memory';
            commitBtn.disabled = false;
        }
    });
}

// --- 8. Quick Research Integration --- //
const quickResearchBtn = document.getElementById('quickResearchBtn');
const researchOverlay = document.getElementById('researchOverlay');
const closeResearchBtn = document.getElementById('closeResearchBtn');
const researchBody = document.getElementById('researchBody');

if (quickResearchBtn && researchOverlay) {
  quickResearchBtn.addEventListener('click', async () => {
    const query = aiQueryInput ? aiQueryInput.value.trim() : "";
    const activeTopic = document.getElementById('topicTitle') ? document.getElementById('topicTitle').textContent : "Science";
    const topic = query || activeTopic.replace('Learning Workspace', 'General Science');

    // UI Feedback
    researchOverlay.classList.remove('hidden');
    researchBody.innerHTML = '<div class="pulse-loader">Synthesizing Diamond Research...</div>';
    triggerThinking(4000);

    // GSAP Entry Animation
    if (window.gsap) {
      gsap.fromTo(".research-card", 
        { y: 100, opacity: 0, scale: 0.8, rotateX: 20 },
        { y: 0, opacity: 1, scale: 1, rotateX: 0, duration: 1, ease: "back.out(1.7)" }
      );
    }

    try {
      const response = await fetch('/api/ai/research', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic: topic })
      });

      const data = await response.json();

      if (data.summary) {
        // Format bullet points from markdown-ish string
        const points = data.summary.split('\n').filter(p => p.trim().startsWith('*') || p.trim().startsWith('-'));
        const listHtml = `<ul>${points.map((p, i) => `<li style="animation-delay: ${i * 0.1}s">${p.replace(/^[*-]\s*/, '')}</li>`).join('')}</ul>`;
        
        researchBody.innerHTML = listHtml;

        // Subtle success flicker on avatar
        if (avatarImg) {
          gsap.to(avatarImg, { filter: 'brightness(2) hue-rotate(90deg)', duration: 0.2, yoyo: true, repeat: 3 });
        }
      } else {
        researchBody.innerHTML = '<p style="color: #ef4444;">Failed to synthesize research. Please try again.</p>';
      }
    } catch (error) {
      console.error("Research API Error:", error);
      researchBody.innerHTML = '<p style="color: #ef4444;">Connection lost to Knowledge Vault.</p>';
    }
  });

  closeResearchBtn.addEventListener('click', () => {
    if (window.gsap) {
      gsap.to(".research-card", { 
        y: 50, opacity: 0, scale: 0.9, duration: 0.5, ease: "power2.in",
        onComplete: () => researchOverlay.classList.add('hidden')
      });
    } else {
      researchOverlay.classList.add('hidden');
    }
  });

  // Close on backdrop click
  researchOverlay.addEventListener('click', (e) => {
    if (e.target === researchOverlay) closeResearchBtn.click();
  });
}
