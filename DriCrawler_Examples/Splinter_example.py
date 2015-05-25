from splinter import Browser

#browser = Browser()
browser = Browser('firefox', user_agent="Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en)")

browser.visit('http://google.com')
browser.fill('q', 'splinter - python acceptance testing for web applications')
browser.find_by_name('btnG').click()

if browser.is_text_present('splinter.cobrateam.info'):
    print "Yes, the official website was found!"
else:
    print "No, it wasn't found... We need to improve our SEO techniques"

browser.quit()