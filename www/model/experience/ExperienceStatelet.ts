
export class ExperienceStatelet
{
  public name: string;

  constructor(
    nameOrSlet: string | ExperienceStatelet,
    public value = true,
    public observable = true
  )
  {
    if (nameOrSlet instanceof ExperienceStatelet) {
      this.name = nameOrSlet.name;
      this.value = nameOrSlet.value;
      this.observable = nameOrSlet.observable;
      return;
    }
    this.name = nameOrSlet;
  }

  public clone(): ExperienceStatelet {
    const retval = new ExperienceStatelet(this.name, this.value, this.observable);
    return retval;
  }

  public equals(other: ExperienceStatelet): boolean {
    const isEqual = this.name === other.name &&
        this.value === other.value &&
        this.observable === other.observable;
    return isEqual;
  }

  public toString(): string {
    // We just need a distinct string to represent ourselves.
    // JSON to the rescue!
    const arr = [
      this.name,
      this.value
    ];
    if (!this.observable) {
      arr.push('hidden');
    }
    const s = JSON.stringify(arr);
    return s;
  }
};
