const params = Object.fromEntries(decodeURIComponent(window.location.search).slice(1).split('&').map(x => x.split('=')));
const step = parseInt(params.step);
const nextUrl = `/place-an-order?step=${step+1}`

let s = loadState();

const next = (go=true) => {
    [...document.querySelectorAll('input')].forEach(e => {
        n = e.name;
        v = e.value;
        if (n && v) {
            s = {
                [n]: v,
                ...s
            }
        }
    });
    saveState(s);
    if (go) {
        document.location = nextUrl;
    }
}

const finalize = () => {
    next(false);
    form = document.getElementById('eticketForm');
    s = localStorage.getItem('state');
    form.innerHTML =
        `<input type="hidden" name="sealedOrderData" value="${s}">`
    form.submit();
}
