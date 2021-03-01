import { Action } from "../agentbody/Action";
import { ExperienceState } from "./ExperienceState";

type CountedState = [ExperienceState, number];

export class ExperienceActionConsequence
{
  private _action: Action;
  private _subsequentStates = new Array<CountedState>();

  constructor(action: Action) {
    this._action = action.clone();
  }

  get action() {
    return this._action.clone();
  }

  private* iterConsequences(): IterableIterator<CountedState> {
    // Create a safe copy so it will not be altered during ieteration.

  }
};
