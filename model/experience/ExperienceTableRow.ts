import { ExperienceActionConsequence } from "./ExperienceActionConsequence";
import { ExperienceState } from "./ExperienceState";

export class ExperienceTableRow
{
  private _state: ExperienceState;
  private _actionConsequences = new Array<ExperienceActionConsequence>();

  public constructor(state: ExperienceState) {
    this._state = state.clone();
  }


};

