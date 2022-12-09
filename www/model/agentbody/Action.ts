
export class Action {
  private _name: string;

  // TODO: Eventually actions will be able to specify a tensor
  // that describes continuous variations of the action such
  // as "where" and "how much". They'll also be able to be
  // linked to sensory inputs, thus making things like saccades
  // possible. But for now, just a string will suffice.

  public constructor(name: string) {
    this._name = name;
  }

  get name() {
    return this._name;
  }
  set name(n: string) {
    this._name = n;
  }

  public clone(): Action {
    const retval = new Action(this._name);
    return retval;
  }

  public equals(other: Action): boolean {
    return other._name === this._name;
  }
};
