const ATJAUNOT = 1000;

async function lasiChatu(){
    const atbilde = await fetch("/chats/lasi");
    const datuObjekts = await atbilde.json();
    raadiChataRindas(datuObjekts);
    await new Promise(resolve => setTimeout(resolve, ATJAUNOT));
    await lasiChatu();
}

function raadiChatuVienkaarshi(dati){
    const jaunaRinda =  "</br>";
    let chats = "";
    let chataDiv = document.getElementById("chats");
    for (let rinda of dati["chats"]){
        chats = chats + rinda + jaunaRinda;
    }
    chataDiv.innerHTML = chats;
}
async function suutiZinju(){
    let zinjasElements = document.getElementById("zinja");
    let zinja = zinjasElements.value;

    //šajā if-ā pārbaudām, vai pirmais ziņas simbols ir /, kas apzīmē komandas sākumu
    if (zinja[0] === '/'){
        if (zinja.substring(1,5)=='nick'){
            //Ja tiek dota komanda /nick un jaunais lietotājvārds

            //Nolasām no html lapas veco niku un saglabājam mainīgajā vecsVards
            let vecsVards = document.getElementById('vards').innerHTML;
            //Nolasām no ziņas jauno niku un saglabājam mainīgajā jaunsVards
            //Nogriežam no visas sūtāmās ziņas nost sākumu /nick 
            let jaunsVards = zinja.substring(6,zinja.length);
            //Ierakstām jauno vārdu cepumā - atrodam cepumu 'lietotajs'
            document.cookie = "lietotajs=" + jaunsVards + "; expires=Thu, 26 Nov 2020 12:00:00 UTC; path=/";
            //Tagad jānomaina lietotājvārds pašā lapā 
            document.getElementById("vards").innerHTML = jaunsVards;
            //Un jānosūta visiem čatā ziņa par to, ka lietotājs nomainījis lietotājvārdu
            zinjasElements.value = "";
            zinja = "Lietotājs " + vecsVards + " tagad zināms kā " + jaunsVards;
            const atbilde = await fetch("/chats/suuti",{
                method: "POST",
                headers:
                {
                    "Content-Type":"application/json"
                },
                body: JSON.stringify({"chats":zinja})
            });
            const datuObjekts = await atbilde.json();
            raadiChataRindas(datuObjekts)
        }
        else if (zinja.substring(1,5)=='away'){
            //Ja tiek dota komanda /away un paziņojums
            let cepumsLietotajs = getCookie('lietotajs');
            //Nogriežam no visas sūtāmās ziņas nost sākumu /away 
            let awayZinja = zinja.substring(6,zinja.length);
            //Sastādām paziņojumu, ka lietotājs ir away + ziņa un parādām kopējā čatā
            zinja = "Lietotājs " + cepumsLietotajs + " ir prom, jo " + "\'" + awayZinja + "\'";
            zinjasElements.value = "";
            const atbilde = await fetch("/chats/suuti",{
                method: "POST",
                headers:
                {
                    "Content-Type":"application/json"
                },
                body: JSON.stringify({"chats":zinja})
            });
            const datuObjekts = await atbilde.json();
            raadiChataRindas(datuObjekts)
        }
        else if (zinja.substring(1,3)=='me'){
            //Ja tiek dota komanda /me un paziņojums
            //Te būs sarežģītāk, jo nāksies mainīt arī ziņas dizainu...
        }
    }
    else{
        zinjasElements.value = "";
        const atbilde = await fetch("/chats/suuti",{
            method: "POST",
            headers:
            {
                "Content-Type":"application/json"
            },
            body: JSON.stringify({"chats":zinja})
        });
        const datuObjekts = await atbilde.json();
        raadiChataRindas(datuObjekts)
    }
}

let ievadesLauks = document.getElementById("zinja");
ievadesLauks.addEventListener("keyup", function(event){
    if(event.keyCode === 13){
        suutiZinju();
    }
})

function raadiChataRindas(dati) {
    const chatUL = document.getElementById("chats");
    // novaacam ieprieksheejo saturu
    while (chatUL.firstChild) {
        chatUL.firstChild.remove();
    }
    for (let rinda of dati["chats"]) {
      chatLI = izveidoJaunuRindu(rinda);
      chatUL.appendChild(chatLI);
    }
    // noskrolleejam uz leju pie peedeejaa chata texta
    var chatScrollBox = chatUL.parentNode;
    chatScrollBox.scrollTop = chatScrollBox.scrollHeight;
  }
  
  
  function izveidoJaunuRindu(zinja) { 
    let newLI = document.createElement("li");
    newLI.className = "left clearfix"
    let newDiv = document.createElement("div"); 
    newDiv.className = "chat-body clearfix"
    let newContent = document.createTextNode(zinja); 
    newLI.appendChild(newDiv); 
    newDiv.appendChild(newContent); 
    return newLI;
  }

  function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }
