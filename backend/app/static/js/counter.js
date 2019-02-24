document.addEventListener('DOMContentLoaded', function () {
   const inputs = document.querySelectorAll('input[type=text], input[type=password], textarea');
   M.CharacterCounter.init(inputs);
 });
