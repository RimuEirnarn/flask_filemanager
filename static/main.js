import "./jquery.js"

function counter() {
    let count = 1
    return [
        () => {
            return count
        },
        () => {
            count++
        }
    ]
}
const [countGet, countSet] = counter()

function delete_file(target) {
    // console.log(target)
    let dataPath = target.attributes['data-path']
    let path = dataPath.nodeValue
    let dataIndex = target.attributes['data-index'].nodeValue
    if (!path) {
        createFlash('error', "Filename cannot be empty!")
        throw new Error("Filename is empty")
    }
    $.ajax({
        method: "DELETE",
        url: "/api/files",
        data: {
            file: path
        },
        success(res) {
            console.log(res)
            const category = res.status
            const message = res.message
            createFlash(category, message)
            if (category == "success") {
                let files = $("#files")
                files.children().eq(dataIndex).hide()
                countSet()
                // console.log(countGet())
                if (countGet() == files.children().length) {
                    files.append(`<div class='list-group-item list-group-item-action disabled'>
                    <span class="text-primary">Empty directory</span>
                </div>`)
                }
            }
        },
    })
}

var sanitizeHTML = function (str) {
    return str.replace(/[^\w. ]/gi, function (c) {
        return '&#' + c.charCodeAt(0) + ';';
    });
};

function createFlash(category, message) {
    let cat = sanitizeHTML(category)
    if (!["error", "success", "warning"].includes(cat)) {
        createFlash('error', "E-INVFLASH")
        console.error(`Cannot create flash, ${cat} is undefined`)
        return
    }
    let mes = sanitizeHTML(message)
    let icon = ""
    let type = cat
    switch (type) {
        case "error":
            icon = '<i class="bi bi-x-circle-fill"></i>'
            break;
        case "success":
            icon = '<i class="bi bi-check-circle-fill"></i>'
            break
        case "warning":
            icon = '<i class="bi bi-exclamation-circle-fill"></i>'
            break
        default:
            break;
    }
    if (type == 'error') type = "danger"
    $("#messages").append(`<div class="alert alert-${type} alert-dismissible fade show" role="alert">
    ${icon}
    ${mes}
  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
</div>
    `)
    let messages = $("#messages")
    if (messages.children().length == 2) {
        messages.children()[0].remove()
    }
}


jQuery(() => {
    console.log("Initialised")
    // createFlash('success', "app initialised")
    let target = $("#files > div > div.row > div.col > div.row > div.col > button")
    if (target) {
        for (const file of target) {
            // console.log(file)
            $(file).on('click', () => delete_file(file))
        }
    }
})
