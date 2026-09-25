/**
 * Newsletter signups, sent straight to MailerLite.
 *
 * Posts to the public endpoint of the "Newsletter signup" embedded form in the
 * MailerLite account (it adds people to the Newsletter group). No API key is
 * involved or exposed: this is the same endpoint MailerLite's own embed code
 * uses. Double opt-in is off: people are added straight away, and a MailerLite
 * automation ("Welcome to the Atlas list") sends them the welcome email.
 *
 * Wired on the homepage ("Join The Atlas List") and the podcast page
 * ("Never Miss an Episode"). Each block needs: an email input, a button and an
 * element with [data-nl-status] for messages, inside an element with [data-nl].
 */
(function () {
  var ENDPOINT = 'https://assets.mailerlite.com/jsonp/2573115/forms/199520945794189126/subscribe';
  var EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

  function say(el, text, state) {
    if (!el) return;
    el.textContent = text;
    el.setAttribute('data-state', state || '');
  }

  function wire(block) {
    var input = block.querySelector('input[type="email"]');
    var button = block.querySelector('button');
    var status = block.querySelector('[data-nl-status]');
    if (!input || !button) return;
    var busy = false;

    function submit(e) {
      if (e) e.preventDefault();
      if (busy) return;
      var email = (input.value || '').trim();
      if (!EMAIL_RE.test(email)) {
        say(status, 'That email address looks incomplete. Please check it and try again.', 'bad');
        input.focus();
        return;
      }
      busy = true;
      button.disabled = true;
      say(status, 'Signing you up\u2026', 'wait');
      var body = new FormData();
      body.append('fields[email]', email);
      body.append('ml-submit', '1');
      body.append('anticsrf', 'true');
      fetch(ENDPOINT, { method: 'POST', body: body })
        .then(function (r) { return r.json().catch(function () { return { success: r.ok }; }); })
        .then(function (res) {
          if (res && res.success) {
            say(status, 'You\u2019re on the list. A welcome email is on its way.', 'ok');
            input.value = '';
          } else {
            var msg = res && res.errors && res.errors.fields && res.errors.fields.email && res.errors.fields.email[0];
            say(status, msg || 'That did not go through. Please try again in a moment.', 'bad');
          }
        })
        .catch(function () {
          say(status, 'That did not go through. Please check your connection and try again.', 'bad');
        })
        .then(function () { busy = false; button.disabled = false; });
    }

    var form = block.tagName === 'FORM' ? block : block.querySelector('form');
    if (form) form.addEventListener('submit', submit);
    else {
      button.addEventListener('click', submit);
      input.addEventListener('keydown', function (e) { if (e.key === 'Enter') submit(e); });
    }
  }

  var blocks = document.querySelectorAll('[data-nl]');
  for (var i = 0; i < blocks.length; i++) wire(blocks[i]);
})();
