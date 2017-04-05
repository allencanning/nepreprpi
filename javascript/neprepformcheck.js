function isValidDate(m,d,y) {
  m = m - 1;
  var composedDate = new Date(y, m, d);
  return composedDate.getDate() == d &&
            composedDate.getMonth() == m &&
            composedDate.getFullYear() == y;
}

function deleteFormCheck() {
  
}

function formCheck() {
  var winner = document.forms['process']['winner'].value;
  var loser = document.forms['process']['loser'].value;
  var ws = document.forms['process']['winner_score'].value;
  var ls = document.forms['process']['loser_score'].value;
  var month = document.forms['process']['month'].value;
  var day = document.forms['process']['day'].value;
  var year = document.forms['process']['year'].value;
  var msg = "";

  if (winner == "" || loser == "") {
    msg = "You must select a team";
  }

  if (winner == loser) {
    msg = msg + "\nWinner cannot equal Loser, please pick a different team";
  }

  if (isNaN(ws)) {
    msg = msg + "\nWinner score must be a number";
  }

  if (isNaN(ls)) {
    msg = msg + "\nLoser score must be a number";
  }

  if (!isValidDate(month,day,year)) {
    msg = msg + "\nYou must enter a valid date";
  } else {
    document.forms['process']['date'].value = month+'/'+day+'/'+year;
  }

  if (msg != "") {
    msg = "Please correct the following errors and resubmit:\n\n" + msg;
    alert(msg);
    return false;
  }
  return true;
}
