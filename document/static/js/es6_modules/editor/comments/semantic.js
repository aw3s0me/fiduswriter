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
        this.autoList = []
        this.origData = {}

        this.downloadMeta()
    }

    /**
     * Downloading metadata (theSoz list) using Ajax
     */
    downloadMeta() {
        jQuery.get('/static/json/soz_lookup.json', data => {
            this.origData = data
            this.autoList = Object.keys(data).map(key => { return { 'value' : key, 'label' : key + '.' + data[key] } })
        }, "json")
        .fail(() => {
            alert("Error occured when downloading theSoz list")
        })
    }

    /**
     * Initializing tag input box using jQueryUI autocomplete
     */
    initTagBoxes() {
        let boxes = jQuery('#comment-box-container').find('.active')

        jQuery.each(boxes, (index, box) => {
            let boxId = this.mod.interactions.getCommentId(box)
            let self = this
            let inputTag = jQuery(box).find('.comment-tags')

            //if this id is already initialized. continue
            if (this.lookupDOM.hasOwnProperty(boxId)) {
                let autcompleteInstance = inputTag.autocomplete("instance")
                if (autcompleteInstance) {
                    return
                }
            }

            this.lookupDOM[boxId] = inputTag
                .bind( "keydown", function( event ) {
                    if ( event.keyCode === jQuery.ui.keyCode.TAB &&
                        jQuery( this ).autocomplete( "instance" ).menu.active ) {
                        event.preventDefault()
                    }
                })
                .autocomplete({
                    source: ( request, response ) => {
                      // delegate back to autocomplete, but extract the last term
                        response( jQuery.ui.autocomplete.filter(
                            this.autoList, this.extractLast( request.term ) ) )
                    },
                    focus: () => {
                      // prevent value inserted on focus
                        return false;
                    },
                    select: function( event, ui ) {
                        let terms = self.split( this.value )
                        // remove the current input
                        terms.pop()
                        // add the selected item
                        terms.push( ui.item.value )
                        // add placeholder to get the comma-and-space at the end
                        terms.push( "" )
                        this.value = terms.join( "; " )
                        return false
                    }}
                )
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

    /**
     * Method to extract last term from autocomplete jquery input
     * @param term
     * @returns {T}
     */
    extractLast(term) {
        return this.split( term ).pop()
    }

    /**
     * Method to separate values in input by ';' symbol
     * @param val
     */
    split(val) {
        return val.split( /;\s*/ )
    }

    /**
     * Check if tags are correct in input
     * @param tagsIds
     * @returns {boolean}
     */
    validateTags(tagsIds) {
        let newTags = []
        for (let value of tagsIds) {
            if (!value || value === "" || value === " ") {
                continue
            }

            if (this.origData.hasOwnProperty(value)) {
                newTags.push(value)
                //return false
            }
        }

        return newTags
        //return true
    }

    getTagsFromHtml(id) {
        if (!id || id === 0 || !this.lookupDOM.hasOwnProperty(id)) {
            return []
        }

        let values = this.lookupDOM[id].val()
        let terms = this.split(values)
        //if (!this.validateTags(terms)) {
        //    return []
        //}

        return this.validateTags(terms)
    }

    /**
     * Adding tags labels after submitting comment
     * @param tags
     */
    addTagBoxtoHtml(tags) {
        console.log(tags)
    }
}