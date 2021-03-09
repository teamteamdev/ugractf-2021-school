serializeState = (dict) => {
    state = (Object.entries(dict).map(
        ([k, v]) => `${k}:${v}`
    )).join(';') + ";hash:";
    state += md5(state);
    console.log(state);
    state = btoa(encodeURIComponent(state));
    return state;
};

deserializeState = (state) => {
    kv = decodeURIComponent(atob(state));
    dict = Object.fromEntries(kv.split(';').map(x => x.split(':')));
    return dict;
}

loadState = () => {
    state = localStorage.getItem('state');
    return deserializeState(state);
}

saveState = (dict) => {
    localStorage.setItem('state', serializeState(dict));
}
