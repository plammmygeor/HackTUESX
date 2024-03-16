const mqttBrokerUrl = 'ohhhhhh-ny7qjv.a01.euc1.aws.hivemq.cloud'; 
const mqttTopic = 'HACKTUESX/QUATRO/SH';
const mqttUsername = 'tester2';
const mqttPassword = '4Dummies';
const mqttPort = 8883;

const mqttClient = mqtt.connect(mqttBrokerUrl, {
  username: mqttUsername,
  password: mqttPassword
});

app.use(express.json());

app.post('/updateState', (req, res) => {
  const { tv, lights, blinds } = req.body;

  const state = tv + lights + blinds;
  const status = getStatus(state);

  const sql = 'INSERT INTO states (tv, lights, blinds, status) VALUES (?, ?, ?, ?)';
  db.query(sql, [tv, lights, blinds, status], (err, result) => {
    if (err) {
      console.error('Error saving state to MySQL database:', err);
      throw err;
    }
    console.log('State saved to MySQL database');
  });

  mqttClient.publish(mqttTopic, JSON.stringify({ tv, lights, blinds, status }));

  res.sendStatus(200);
});

function getStatus(state) {
  let status;
  switch(state) {
    case 0: status = "all off"; break;
    case 2: status = "lamp on"; break;
    case 1: status = "tv on"; break;
    case 4: status = "blinds on"; break;
    case 3: status = "lamp and tv on"; break;
    case 6: status = "lamp and blinds on"; break;
    case 5: status = "tv and blinds on"; break;
    case 7: status = "all on"; break;
    default: status = "unknown"; break;
  }
  return status;
}

function updateState() {
  const tv = document.querySelector('#tv').checked ? 1 : 0;
  const lights = document.querySelector('#lights').checked ? 2 : 0;
  const blinds = document.querySelector('#blinds').checked ? 4 : 0;

  const state = tv + lights + blinds;

  let status;
  switch(state) {
    case 0: status = "all off"; break;
    case 2: status = "lamp on"; break;
    case 1: status = "tv on"; break;
    case 4: status = "blinds on"; break;
    case 3: status = "lamp and tv on"; break;
    case 6: status = "lamp and blinds on"; break;
    case 5: status = "tv and blinds on"; break;
    case 7: status = "all on"; break;
    default: status = "unknown"; break;
  }

  document.getElementById("output").textContent = "Status: " + status;
  
  if (lights === 2) {
    document.getElementById("image").src = "/static/sully_lamp_light.png"; // Change the src attribute to the new image path
  } else {
    document.getElementById("image").src = "/static/sully_lamp.png"; // Revert to the original image when lights are turned off
  }

  saveState();
}

function saveState() {
  const tvState = document.querySelector('#tv').checked;
  const lightsState = document.querySelector('#lights').checked;
  const blindsState = document.querySelector('#blinds').checked;

  localStorage.setItem('tvState', tvState);
  localStorage.setItem('lightsState', lightsState);
  localStorage.setItem('blindsState', blindsState);
}

function loadState() {
  const tvState = localStorage.getItem('tvState') === 'true';
  const lightsState = localStorage.getItem('lightsState') === 'true';
  const blindsState = localStorage.getItem('blindsState') === 'true';

  document.querySelector('#tv').checked = tvState;
  document.querySelector('#lights').checked = lightsState;
  document.querySelector('#blinds').checked = blindsState;

  updateState();
}
