serializeState = (dict) => {
    state = (Object.entries(dict).map(
        ([k, v]) => `${k}:${v}`
    )).join(';');
    state = btoa(encodeURIComponent(state));
    return state;
};

deserializeState = (state) => {
    kv = decodeURIComponent(atob(state));
    dict = Object.fromEntries(kv.split(';').map(x => x.split(':')));
    console.log(dict);
    return dict;
}

loadState = () => {    
    state = localStorage.getItem('state');
    return deserializeState(state);
}

saveState = (dict) => {
    localStorage.setItem('state', serializeState(dict));
}
