import { ExperienceStatelet } from "~/model/experience/ExperienceStatelet";

describe('ExperienceStatelet', () => {
  describe('constructor', () => {
    test('should be instantiable with explicit values.', () => {
      const esl = new ExperienceStatelet('alpha', true, false);
      expect(esl).not.toBeNull();
      expect(esl.name).toBe('alpha');
      expect(esl.value).toBe(true);
      expect(esl.observable).toBe(false);
    });

    test('should be instantiable with implicit values.', () => {
      const esl = new ExperienceStatelet('alpha');
      expect(esl).not.toBeNull();
      expect(esl.name).toBe('alpha');
      expect(esl.value).toBe(true);
      expect(esl.observable).toBe(true);
    });

    test('should be instantiable with a copy constructor.', () => {
      const esl = new ExperienceStatelet('alpha', true, false);
      const esl2 = new ExperienceStatelet(esl);
      expect(esl2).not.toBeNull();
      expect(esl2.name).toBe('alpha');
      expect(esl2.value).toBe(true);
      expect(esl2.observable).toBe(false);
    });
  });

  describe('equals, clone, and toString', () => {
    test('should be equal if all arguments are equal.', () => {
      const esl = new ExperienceStatelet('alpha', true, false);
      const esl2 = new ExperienceStatelet('alpha', true, false);
      expect(esl.equals(esl2)).toBeTruthy();
    });

    test('should be equal if instantiated through copy.', () => {
      const esl = new ExperienceStatelet('alpha', true, false);
      const esl2 = new ExperienceStatelet(esl);
      expect(esl.equals(esl2)).toBeTruthy();
    });

    test('should be equal if cloned.', () => {
      const esl = new ExperienceStatelet('alpha', true, false);
      const esl2 = esl.clone();
      expect(esl.equals(esl2)).toBeTruthy();
    });

    test('should ensure that equality is reciprocal.', () => {
      const esl = new ExperienceStatelet('alpha', true, false);
      const esl2 = esl.clone();
      expect(esl2.equals(esl)).toBeTruthy();
    });

    test('should have equal strings if equal values.', () => {
      const esl = new ExperienceStatelet('alpha', true, false);
      const esl2 = esl.clone();
      expect(esl.toString()).toEqual(esl2.toString());
    });

    test('should not be equal if name is different.', () => {
      const esl = new ExperienceStatelet('alpha', true, false);
      const esl2 = esl.clone();
      esl2.name = 'beta';
      expect(esl2.equals(esl)).toBeFalsy();
    });

    test('should not be equal if value is different.', () => {
      const esl = new ExperienceStatelet('alpha', true, false);
      const esl2 = esl.clone();
      esl2.value = false;
      expect(esl2.equals(esl)).toBeFalsy();
    });

    test('should not be equal if observability is different.', () => {
      const esl = new ExperienceStatelet('alpha', true, false);
      const esl2 = esl.clone();
      esl2.observable = true;
      expect(esl2.equals(esl)).toBeFalsy();
    });

    test('should have different strings if not equal.', () => {
      const esl = new ExperienceStatelet('alpha', true, false);
      const esl2 = esl.clone();
      esl2.observable = true;
      expect(esl2.toString()).not.toEqual(esl.toString());
    });

    test('should ensure that toString is used for string coercion.', () => {
      const esl = new ExperienceStatelet('alpha', true, false);
      expect(esl.toString()).toEqual(`${esl}`);
      expect(esl.toString()).toEqual(esl + '');
    });
  });
});
