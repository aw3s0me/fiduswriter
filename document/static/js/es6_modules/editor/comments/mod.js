import {ModCommentStore} from "./store"
import {ModCommentLayout} from "./layout"
import {ModCommentInteractions} from "./interactions"
import {ModCommentSemantic} from "./semantic"

export class ModComments {
    constructor(editor) {
        editor.mod.comments = this
        this.editor = editor
        new ModCommentStore(this)
        new ModCommentLayout(this)
        new ModCommentInteractions(this)
        new ModCommentSemantic(this)
    }
}
