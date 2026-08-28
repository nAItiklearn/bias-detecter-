const textInput = document.getElementById("text-input");
const analyzeButton = document.getElementById("analyze-button");
const clearButton = document.getElementById("clear-button");
const resultsSection = document.getElementById("results");
const wordCount = document.getElementById("word-count");

//word count

textInput.addEventListener("input", () => {
    const text = textInput.value.trim();
    if(!text){
        wordCount.textContent="0 words";
        return;
    }
        const words = text.split(/\s+/);
        wordCount.textContent =
            `${words.length} ${words.length === 1 ? "word" : "words"}`;

});

//clear button

clearButton.addEventListener("click", () => {
    textInput.value = "";
    wordCount.textContent = "0 words";
    resultsSection.hidden = true;
    textInput.focus();
});

//analyze button
analyzeButton.addEventListener("click", async () => {
    const text= textInput.value.trim();
    if(!text){
        alert("please enter some text first");
        return;
    }
    // button loading state
    analyzeButton.disabled=true;
    analyzeButton.querySelector("span:first-child").textContent=
    "have patience gng..";

    try{
        const response = await fetch("/analyze", {
            method:"POST",
            headers:{
                "Content-Type":"application/json"

            },
            body:JSON.stringify({
                text:text
            })
        });
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.error || "oops something went wrong");}
            displayResults(result);
            
        }
        catch(error){
            console.error(error);
            alert(error.message);

        }finally{
            analyzeButton.disabled=false;
            analyzeButton.querySelector("span:first-child").textContent=
            "Analyze Text";

        }
});

//display results
function displayResults(result){
    resultsSection.hidden=false;

    document.getElementById("bias-score").textContent =
      result.bias_score;

    document.getElementById("score-circle-value").textContent=
      result.bias_score;

    document.getElementById("bias-level").textContent=
       result.bias_level.toUpperCase();
   //signal counts
    const emotionalCount=
     result.emotional_words.length;
    const sensationalCount=
     result.sensational_words.length;
    const loadedCount=
     result.loaded_words.length; 
    const urgencyCount=
     result.urgency_words.length;
    const absoluteCount =
        result.absolute_words.length;

    document.getElementById("emotional-count").textContent=
     emotionalCount;
    document.getElementById("sensational-count").textContent=
     sensationalCount;
    document.getElementById("loaded-count").textContent=
     loadedCount;
    document.getElementById("absolute-count").textContent=
     absoluteCount;
    document.getElementById("urgency-count").textContent=
     urgencyCount;

    //progress bars
    document.getElementById("emotional-bar").style.width=
      `${Math.min(emotionalCount*20, 100)}%`;
        document.getElementById("sensational-bar").style.width=
            `${Math.min(sensationalCount * 25, 100)}%`;
        document.getElementById("absolute-bar").style.width=
            `${Math.min(absoluteCount * 20, 100)}%`;
    document.getElementById("loaded-bar").style.width=
     `${Math.min(loadedCount*20, 100)}%`;
    document.getElementById("urgency-bar").style.width=
     `${Math.min(urgencyCount*20, 100)}%`;
    
    //detected wods
    displayDetectedWords(result);

    //sentiment
     document.getElementById("positive-score").textContent=
         result.Sentiment.positive.toFixed(2);
     document.getElementById("neutral-score").textContent=
         result.Sentiment.neutral.toFixed(2);
    document.getElementById("negative-score").textContent=
         result.Sentiment.negative.toFixed(2);
    
    //NRC emotions

    document.getElementById("anger").textContent=
       result.emotions.anger;
    document.getElementById("fear").textContent=
      result.emotions.fear;
    document.getElementById("surprise").textContent=
      result.emotions.surprise;
    document.getElementById("joy").textContent=
       result.emotions.joy;
    document.getElementById("sadness").textContent=
       result.emotions.sadness;
    document.getElementById("disgust").textContent=
       result.emotions.disgust;

    // scroll to results
    resultsSection.scrollIntoView({
        behavior:"smooth"
    });

}
// detected word tags
function displayDetectedWords(result){
    const container=
        document.getElementById("detected-words");
    container.innerHTML="";

    const categories=[
        {
            words:result.emotional_words,
            className:"emotional"
        },
        {
            words:result.sensational_words,
            className:"sensational"
        },
        {
            words:result.absolute_words,
            className:"absolute"
        },
        {
            words:result.loaded_words,
            className:"loaded"
        },
        {
            words:result.urgency_words,
            className:"urgency"
        },
        {
            words:result.manipulative_words,
            className:"manupilative"
        }
    ];
    const added= new Set();
    categories.forEach(category => {
        category.words.forEach(word => {
            const normalized=
                word.toLowerCase();
            if(added.has(normalized)){
                return;
            }
            added.add(normalized);
            const tag=
                 document.createElement("span");
            tag.className=
                `word-tag ${category.className}`;
            tag.textContent=
                  word;
            container.appendChild(tag)
        });
    });
    if(container.children.length===0){
        const empty=
            document.createElement("span");
        empty.className=
            "no-signals";
        empty.textContent=
           "no obvious linguistic signals detected";
        container.appendChild(empty);
    }
}

