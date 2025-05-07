document.addEventListener("DOMContentLoaded", function () {
    // Get all question elements
    const questions = document.querySelectorAll(".questions");


    const firstAnswer = questions[0].nextElementSibling;
    firstAnswer.style.display = "block";
    let firstanscolor=questions[0];
    firstanscolor.style.background="#D18C3C";


    // Add click event listener to each question
    questions.forEach(function (question) {
        question.addEventListener("click", function () {
         
            const answer = question.nextElementSibling;
            if (answer.style.display === "none" || answer.style.display === "") {
                answer.style.display = "block"; // Show answer
                question.querySelector("::after").textContent = "-"; // Change to '-' when open
            } else {
                answer.style.display = "none"; // Hide answer
                question.querySelector("::after").textContent = "+"; // Change to '+' when closed
            }
        });
    });
});
