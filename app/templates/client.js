document.addEventListener('DOMContentLoaded', function() {
    loadState();
  });
  
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
  
    // Save state to database
    saveStateToDatabase(tv, lights, blinds, status);
  }
  
  function saveStateToDatabase(tv, lights, blinds, status) {
    // Send a POST request to the server
    fetch('/updateState', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ tv, lights, blinds, status })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to save state to the server.');
      }
      console.log('State saved to the server successfully.');
    })
    .catch(error => {
      console.error('Error saving state to the server:', error);
    });
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
  