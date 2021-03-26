let lastInput = 0;

const handlePress = e => {
    e.preventDefault();
    now = Date.now()
    // 6 ms is the world record. no way a user types faster
    if (now - lastInput < 6) {
        alert("Обнаружена попытка накрутки скорости печати. Игра всё.");
        socket.close();
    }
    lastInput = now;
    socket.send(e.charCode);
};

const handleMessage = e => {
    json = JSON.parse(e.data)
    stats = ["mistakes", "avg", "accuracy"]
    stats.forEach(s => {
        value = json[s]
        if (s !== "mistakes") {
            value = value.toFixed(2)
        }
        if (s == "accuracy") {
            value = Math.ceil(value * 100) + '%'
        }
        document.getElementById(s).innerHTML = value
    })
    document.getElementById('text').innerHTML = Array.from(json.text)
        .map((char, i) => {
            if (char == '\n') char = '<br>'
            if (json.cursor > i) {
                return `<span class="entered">${char}</span>`
            } else if (json.cursor == i) {
                return `<span class="current">${char}</span>`
            } else {
                return `${char}`
            }
        }).join('')
    w = document.querySelector('.players').clientWidth - 98;
    document.getElementById('player').style.left = json.cursor / json.text.length * w + 'px'
    document.getElementById('opponent').style.left = json.opponent_cursor / json.text.length * w + 'px'    
    if (json.status == 'finish') {
        if (json.cursor > json.opponent_cursor) {
            alert('Вы выиграли! Вот ваш приз: ' + json.prize);
        } else {
            alert('Вы проиграли! Давайте ещё..')
        }
        socket.close()
    }
};

const err = (e = {}) => {
    if (!e.wasClean) {
        alert('Ошибка!')
    }
};

const socket = new WebSocket(`${window.location.href.replace('http', 'ws')}ws`);
socket.onclose = e => err(e);
socket.onerror = e => err(e);
socket.onmessage = handleMessage;

document.body.onkeypress = handlePress;
