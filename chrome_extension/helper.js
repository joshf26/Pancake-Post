function format_date(date) {
    const day = date.getDay();
    const month = date.getMonth();
    const year = date.getFullYear();
    const hour = date.getHours();
    const minute = date.getMinutes();

    return `${month}/${day}/${year} ${hour}:${minute}`;
}