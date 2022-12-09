import { Action } from "../agentbody/Action";
import { ExperienceState } from "./ExperienceState";

type StateWithCount = {state: ExperienceState, count: number};

export class ExperienceActionConsequence
{
  private _action: Action;
  private _subsequentStates = new Array<StateWithCount>();

  public constructor(action: Action) {
    this._action = action.clone();
  }

  public get action() {
    return this._action.clone();
  }

  public recordConsequence(exst: ExperienceState) {
    // First we increment everything that matches.
    this._subsequentStates.forEach(stc => {
      if (!stc.state.matches(exst)) {
        return;
      }
      stc.count++;
    });

    // Next we find if a state is equal. If no such state is found,
    // then we add it to our log.
    const atLeastOneEquals = this._subsequentStates.some(stc => stc.state.equals(exst));
    if (!atLeastOneEquals) {
      this._subsequentStates.push({
        state: exst.clone(),
        count: 1
      });
    }
  }

  public clone(): ExperienceActionConsequence {
    const retval = new ExperienceActionConsequence(this._action);
    this._subsequentStates.forEach((StateWithCount) => {
      const cst = {
        count: StateWithCount.count,
        state: StateWithCount.state.clone()
      };
      retval._subsequentStates.push(cst);
    });
    return retval;
  }

  private* iterConsequences(): IterableIterator<StateWithCount> {
    // Create a safe copy so it will not be altered during iteration.
    const safecopy = this.clone();
    for (let cst of safecopy._subsequentStates) {
      yield cst;
    }
  }

  public get consequences(): IterableIterator<StateWithCount> {
    return this.iterConsequences();
  }


};
