import { ExperienceStatelet } from "./ExperienceStatelet";

export class ExperienceState
{
  private _statelets = {} as {[name: string]: ExperienceStatelet};

  public constructor(initObservableStatelets?: {[name: string]: boolean})
  {
    if (!initObservableStatelets) {
      return;
    }
    Object.entries(initObservableStatelets).forEach(([name, value]) => {
      this.setStatelet(name, value);
    });
  }

  public clone(): ExperienceState {
    const expst = new ExperienceState();
    Object.entries(this._statelets).forEach(([name, estl]) => {
      expst._statelets[name] = estl.clone();
    });
    return expst;
  }

  private *iterStatelets(): IterableIterator<ExperienceStatelet> {
    // Create a copy of the map for safety, lest it change during iteration.
    const safeclone = this.clone();
    const names = Object.keys(safeclone._statelets).sort();
    for (let name of names) {
      yield safeclone._statelets[name];
    }
  }

  /**
   * Stably iterate over the statelets. Should be safe from change during iteration.
   */
  public get statelets() {
    return this.iterStatelets();
  }

  public setStatelet(nameOrEstl: string | ExperienceStatelet, value = true, observable = true): void
  {
    if (nameOrEstl instanceof ExperienceStatelet) {
      this._statelets[nameOrEstl.name] = nameOrEstl.clone();
      return;
    }

    let estl = new ExperienceStatelet(nameOrEstl, value, observable);
    this._statelets[nameOrEstl] = estl;
  }

  public getStatelet(name: string): ExperienceStatelet | null
  {
    const estl = this._statelets[name];
    if (!estl) {
      return null;
    }
    return estl.clone();
  }

  /**
   * True iff the other state either DOES match or COULD match, e.g. if all of
   * the properties whose values we define, are also defined in the same way
   * in the other state. That is, insofar as this other state intersects with
   * us, there are no contradictions in the intersection.
   * @param other The other experience state that we might match with.
   */
  public matches(other: ExperienceState): boolean
  {
    for (let [name, esl] of Object.entries(this._statelets)) {
      const eslOther = other._statelets[name];
      if (!eslOther) {
        continue;
      }
      if (!esl.equals(eslOther)) {
        return false;
      }
    }
    return true;
  }

  /**
   * True iff every property we define is also defined with the same
   * value in the other state, and vice versa.
   * @param other The other experience state that we might match with.
   */
  public equals(other: ExperienceState): boolean
  {
    const names = [...new Set([
      ...Object.keys(this._statelets),
      ...Object.keys(other._statelets)
    ])];

    for (let name of names) {
      const eslOurs = this._statelets[name];
      const elsTheirs = other._statelets[name];
      if (!eslOurs || !elsTheirs) {
        // It can't be null in both otherwise it wouldn't show up in our names
        // list in the first place. So it's null in one but not the other,
        // which makes them unequal.
        return false;
      }
      if (!eslOurs.equals(elsTheirs)) {
        return false;
      }
    }
    return true;
  }


  /**
   * Produces a stable ordered string. Two experience states that are
   * equal should produce the same string.
   */
  public toString(): string
  {
    // Very similar to the iterator, but we don't need to create safe copies.
    let s = '';
    Object.keys(this._statelets).sort().forEach(name => {
      const esl = this._statelets[name];
      s += esl.toString();
    });
    return s;
  }
};
