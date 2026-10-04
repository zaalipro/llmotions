// Run against a served site: ego-browser nodejs < tools/test_release_layout.mjs
// Optionally prepend `const releaseLayoutConfig = { spaceId: 11, baseURL: 'http://127.0.0.1:8790' };`
// to reuse this task's space or change the site. Otherwise the test owns and closes a space.
const options = typeof releaseLayoutConfig === 'undefined' ? {} : releaseLayoutConfig;
const existingSpace = options.spaceId;
const task = await taskSpace(existingSpace ?? 'ncode release layout test');
const page = task.page('p1');
console.log({ spaceId: task.spaceId });
const results = [];
try {
    for (const width of [320, 390, 768]) {
        await page.cdp('Emulation.setDeviceMetricsOverride', {
            width, height: 844, deviceScaleFactor: 1, mobile: true,
        });
        await page.goto(new URL('/releases/', options.baseURL || 'http://127.0.0.1:8790').href);
        await page.waitForLoadState();
        await page.waitForFunction(() => document.fonts.status === 'loaded');
        const result = await page.evaluate(() => ({
            title: document.title,
            width: document.documentElement.clientWidth,
            contentWidth: document.documentElement.scrollWidth,
            checksums: (document.querySelector('.d-article')?.textContent || '').match(/[0-9a-f]{64}/g) || [],
        }));
        results.push(result);
        if (result.title !== 'ncode releases' || result.checksums.length < 2) {
            throw new Error('Release page or artifact checksums are missing.');
        }
        if (result.contentWidth > result.width + 1) {
            throw new Error(`Release checksums overflow at ${width}px: ${result.contentWidth}px content.`);
        }
    }
    console.log({ passed: true, results });
} finally {
    await page.cdp('Emulation.clearDeviceMetricsOverride', {});
    if (!existingSpace) await task.finish({ keep: [] });
}
