import { Action } from "../agentbody/Action";
import { ExperienceActionConsequence } from "./ExperienceActionConsequence";
import { ExperienceState } from "./ExperienceState";

export class ExperienceTableRow
{
  private _stateFrom: ExperienceState;
  private _actionConsequences = new Array<ExperienceActionConsequence>();

  public constructor(stateFrom: ExperienceState) {
    this._stateFrom = stateFrom.clone();
  }

  public get stateFrom(): ExperienceState {
    return this._stateFrom.clone();
  }

  private findActionEntry(action: Action): ExperienceActionConsequence | null {
    for (let exacque of this._actionConsequences) {
      if (exacque.action.equals(action)) {
        return exacque;
      }
    }
    return null;
  }

  public lookupAction(action: Action): ExperienceActionConsequence {
    let exaque = this.findActionEntry(action);
    if (exaque === null) {
      exaque = new ExperienceActionConsequence(action);
    }
    return exaque;
  }

  public recordAction(action: Action, consequence: ExperienceState): ExperienceActionConsequence {
    let exaque = this.findActionEntry(action);
    if (exaque === null) {
      exaque = new ExperienceActionConsequence(action);
      this._actionConsequences.push(exaque);
    }
    exaque.recordConsequence(consequence);
    return exaque;
  }

  public clone(): ExperienceTableRow {
    const retval = new ExperienceTableRow(this._stateFrom);
    this._actionConsequences.forEach(exaque => {
      const exaque2 = exaque.clone();
      retval._actionConsequences.push(exaque2);
    });
    return retval;
  }

  public *iterActions(): IterableIterator<ExperienceActionConsequence> {
    const safecopy = this.clone();
    for (let exaque of safecopy._actionConsequences) {
      // It's probably not strictly necessary to yield a clone of a clone,
      // but there's no denying it's pretty safe.
      yield exaque.clone();
    }
  }

  public get actions(): IterableIterator<ExperienceActionConsequence> {
    return this.iterActions();
  }
};

