export default {

    checkInput(tab) {
        var i = 0;
        for(var key in tab){
            if (tab[key] == '') {
                i++;
            }
        }
        if (i <= 1)
            return true;
        else
            return false
    },

    checkInput1(tab) {
        var i = 0;
        for(var key in tab){
            if (tab[key] == '') {
                i++;
            }
        }
        if (i == 0)
            return true;
        else
            return false
    },

    ip: 'https://api.statfive.fr/',

}
