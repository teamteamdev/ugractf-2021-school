[...document.querySelectorAll('.flight-choice')].map(e =>
    e.onclick = () => pickFlight(e)
);
localStorage.clear();

const pickFlight = (flight) => {
    document.querySelector('button').disabled = false;
    [...document.querySelectorAll('.flight-choice')].map(e =>
        e.classList.remove('flight-choice_chosen')
    );
    flight.classList.add('flight-choice_chosen');
}

const setFlight = () => {
    flight = document.querySelector('.flight-choice_chosen');
    ds = flight.dataset;
    saveState({
        'from': ds.city,
        'to': ds.dcity,
        'date': ds.date,
        'number': ds.number    
    });
    [from, to, number, date] = [ds.city, ds.dcity, ds.number, ds.date].map(x => encodeURIComponent(x));
    document.location = `/place-an-order?step=2&from=${from}&to=${to}&number=${number}&date=${date}`;
}
