/**
 * Created by alex on 23.04.16.
 */

/**
 * Class for adding semantics to comments
 */
export class ModCommentSemantic {
    constructor(mod) {
        mod.interactions = this
        this.mod = mod
        //Taken from thesoz thesaurus
        //TODO: download thesoz using ajax
    }
}