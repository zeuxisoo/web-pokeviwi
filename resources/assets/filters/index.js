export function pokemonIcon(pokemonId) {
    return "static/assets/img/icons/" + pokemonId + ".png"
}

export function formatPercentage(value) {
    return Math.round(value * 100);
}

export function formatName(value) {
    let string = value.replace(/\_/g, " ").replace("FAST", "").toLowerCase();

    //
    let pieces = string.split(" ");

    for (let i=0; i<pieces.length; i++) {
        let j = pieces[i].charAt(0).toUpperCase();

        pieces[i] = j + pieces[i].substr(1);
    }

    return pieces.join(" ");
}
