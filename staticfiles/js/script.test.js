/**
 * @jest-environment jsdom
 */

const { toggleReply } = require('./script.js');

describe('toggleReply', () => {

    beforeEach(() => {
        document.body.innerHTML = '';
    });

    test('shows a hidden element by setting display to block', () => {
        document.body.innerHTML = '<div id="reply-1" style="display: none;"></div>';
        toggleReply('reply-1');
        const el = document.getElementById('reply-1');
        expect(el.style.display).toBe('block');
    });

    test('hides a visible element by setting display to none', () => {
        document.body.innerHTML = '<div id="reply-1" style="display: block;"></div>';
        toggleReply('reply-1');
        const el = document.getElementById('reply-1');
        expect(el.style.display).toBe('none');
    });

    test('hides an element with no inline display style set', () => {
        // When display is unset, el.style.display returns '' which is not 'none',
        // so the ternary treats it as visible and sets display to 'none'
        document.body.innerHTML = '<div id="reply-1"></div>';
        toggleReply('reply-1');
        const el = document.getElementById('reply-1');
        expect(el.style.display).toBe('none');
    });

    test('toggles back and forth correctly', () => {
        document.body.innerHTML = '<div id="reply-1" style="display: none;"></div>';
        const el = document.getElementById('reply-1');

        toggleReply('reply-1');
        expect(el.style.display).toBe('block');

        toggleReply('reply-1');
        expect(el.style.display).toBe('none');

        toggleReply('reply-1');
        expect(el.style.display).toBe('block');
    });

    test('works independently on multiple elements', () => {
        document.body.innerHTML = `
            <div id="reply-1" style="display: none;"></div>
            <div id="reply-2" style="display: block;"></div>
        `;
        toggleReply('reply-1');
        toggleReply('reply-2');
        expect(document.getElementById('reply-1').style.display).toBe('block');
        expect(document.getElementById('reply-2').style.display).toBe('none');
    });

});