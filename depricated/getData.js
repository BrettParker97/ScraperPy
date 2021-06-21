r2 = []
for (var i = 2; i < r.length; i++)
{
    r2.push(r[i].cells[0].lastChild.getAttribute("href") + "\n");
}
a = new Blob(r2, {type: 'text/plain', endings: 'native'})
newLink.href = window.webkitURL.createObjectURL(a)
newLink.click()