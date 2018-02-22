function getReadableHashRateString(hashrate) {
    var i = 0;
    var byteUnits = [' H', ' KH', ' MH', ' GH', ' TH', ' PH'];
    while (hashrate > 1024) {
        hashrate = hashrate / 1024;
        i++;
    }
    return hashrate.toFixed(2) + byteUnits[i];
}
