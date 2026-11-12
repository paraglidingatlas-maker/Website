/**
 * Google Form -> MailerLite, on every submission (chat 23, 12 Nov 2026).
 *
 * The newsletter form linked from the YouTube descriptions (https://forms.gle/PN3LGt8L589cmugT7) stays as it is;
 * this script, attached to that form, adds each new respondent to MailerLite straight away.
 *
 * Set up once (about 5 minutes, in the owner's own Google account):
 *  1. MailerLite > Integrations > API > "Generate new token" (name it "Google Form"). Copy it. Never paste it in a chat.
 *  2. Open the form in Google Forms > three dots (top right) > "Apps Script". Delete what is there, paste this file.
 *  3. Project Settings (gear) > Script properties > Add: MAILERLITE_TOKEN = the token from step 1.
 *     Optional: MAILERLITE_GROUP = a MailerLite group id, to put form signups in their own group.
 *  4. Triggers (clock icon) > Add trigger > function onFormSubmit, event source "From form", event type
 *     "On form submit" > Save, and allow the access Google asks for.
 *  5. Optional, once: run backfillAll (Run menu) to add everyone who already answered the form.
 *
 * What it reads: the email from a question whose title contains "mail" (or the form's own "collect email
 * addresses" setting), the name from a question whose title contains "name". Nothing else is sent.
 */

function onFormSubmit(e) {
  addToMailerLite_(readResponse_(e.response));
}

function backfillAll() {
  var form = FormApp.getActiveForm();
  var all = form.getResponses();
  var ok = 0;
  all.forEach(function (r) { if (addToMailerLite_(readResponse_(r))) ok++; });
  Logger.log('Backfill: %s of %s responses sent to MailerLite', ok, all.length);
}

function readResponse_(response) {
  var out = { email: (response.getRespondentEmail && response.getRespondentEmail()) || '', name: '' };
  response.getItemResponses().forEach(function (ir) {
    var title = ir.getItem().getTitle().toLowerCase();
    var value = String(ir.getResponse() || '').trim();
    if (!out.email && title.indexOf('mail') !== -1) out.email = value;
    else if (!out.name && title.indexOf('name') !== -1) out.name = value;
  });
  return out;
}

function addToMailerLite_(person) {
  if (!person.email || person.email.indexOf('@') === -1) return false;
  var props = PropertiesService.getScriptProperties();
  var token = props.getProperty('MAILERLITE_TOKEN');
  if (!token) throw new Error('Set the script property MAILERLITE_TOKEN first (see the top of this file).');
  var body = { email: person.email.toLowerCase() };
  if (person.name) body.fields = { name: person.name };
  var group = props.getProperty('MAILERLITE_GROUP');
  if (group) body.groups = [group];
  // POST /api/subscribers creates the subscriber, or updates one that already exists (no duplicates).
  var res = UrlFetchApp.fetch('https://connect.mailerlite.com/api/subscribers', {
    method: 'post',
    contentType: 'application/json',
    headers: { Authorization: 'Bearer ' + token, Accept: 'application/json' },
    payload: JSON.stringify(body),
    muteHttpExceptions: true
  });
  var code = res.getResponseCode();
  if (code !== 200 && code !== 201) {
    Logger.log('MailerLite %s for %s: %s', code, body.email, res.getContentText().slice(0, 300));
    return false;
  }
  return true;
}
