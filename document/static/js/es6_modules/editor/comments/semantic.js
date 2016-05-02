/**
 * Created by alex on 23.04.16.
 */

/**
 * Class for adding semantics to comments
 */
export class ModCommentSemantic {
    constructor(mod) {
        mod.semantic = this
        this.mod = mod
        this.filter = []
        this.lookupFilter = {}
        this.lookupDOM = {}

        this.downloadMeta()
    }

    /**
     * Downloading metadata (theSoz list) using Ajax
     */
    downloadMeta() {
        jQuery.get('/static/json/soz_lookup.json', data => {
            this.autoList = Object.keys(data).map(key => { return key + " : " + data[key] })
        }, "json")
        .fail(() => {
            alert("Error occured when downloading theSoz list")
        })
    }

    /**
     * Initializing tag input box using jQueryUI autocomplete
     * @todo complete method
     */
    initTagBoxes() {
        let boxes = jQuery('#comment-box-container').find('.active')

        jQuery.each(boxes, (index, box) => {
            let boxId = this.mod.interactions.getCommentId(box)

            //if this id is already initialized. continue
            if (this.lookupDOM.hasOwnProperty(boxId)) {
                return true
            }

            this.lookupDOM[boxId] = $(box).find('.comment-tags').autocomplete({
                source: this.autoList
            })
        })
    }

    /**
     * Cleaning resources for autocomplete by node
     * @param id
     */
    removeTagBox(id) {
        //let boxId = this.mod.interactions.getComment(box.get(0))
        if (!this.lookupDOM.hasOwnProperty(id)) {
            return false
        }

        this.lookupDOM[id].autocomplete("destroy")
        delete this.lookupDOM[id]

        return true
    }

}