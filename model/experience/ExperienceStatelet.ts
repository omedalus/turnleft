
export class ExperienceStatelet
{
  constructor(
    public name: string,
    public value: boolean,
    public observable: boolean
  )
  {
  }

  public clone(): ExperienceStatelet {
    const retval = new ExperienceStatelet(this.name, this.value, this.observable);
    return retval;
  }
};
