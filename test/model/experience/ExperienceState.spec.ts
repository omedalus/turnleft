import { ExperienceState } from "~/model/experience/ExperienceState";

describe('ExperienceState', () => {
  describe('constructor', () => {
    test('should be instantiable with an empty call.', () => {
      const estate = new ExperienceState();
      expect(estate).not.toBeNull();
    });

    test('should have observable statelets that it is instantiated with.', () => {
      const estate = new ExperienceState({
        'alpha': true,
        'beta': false,
        'gamma': false
      });

      const estAlpha = estate.getStatelet('alpha');
      expect(estAlpha).not.toBeNull();
      expect(estAlpha?.name).toBe('alpha');
      expect(estAlpha?.value).toBe(true);
      expect(estAlpha?.observable).toBe(true);

      const estBeta = estate.getStatelet('beta');
      expect(estBeta).not.toBeNull();
      expect(estBeta?.name).toBe('beta');
      expect(estBeta?.value).toBe(false);
      expect(estBeta?.observable).toBe(true);

      const estGamma = estate.getStatelet('gamma');
      expect(estGamma).not.toBeNull();
      expect(estGamma?.name).toBe('gamma');
      expect(estGamma?.value).toBe(false);
      expect(estGamma?.observable).toBe(true);
    });

    test('should contain all specified statelets, and only such statelets.', () => {
      const estate = new ExperienceState({
        'gamma': false,
        'alpha': true,
        'beta': false
      });

      const keysFound = [];
      for (let est of estate.statelets) {
        keysFound.push(est.name);
      }

      expect(keysFound).toContain('alpha');
      expect(keysFound).toContain('beta');
      expect(keysFound).toContain('gamma');
      expect(keysFound).toHaveLength(3);
    });
  });

  describe('setters and getters', () => {
    test('should get what was set.', () => {
      const estate = new ExperienceState();
      estate.setStatelet('gamma', false, false);
      estate.setStatelet('alpha', true);
      estate.setStatelet('beta', false);

      const estAlpha = estate.getStatelet('alpha');
      expect(estAlpha).not.toBeNull();
      expect(estAlpha?.name).toBe('alpha');
      expect(estAlpha?.value).toBe(true);
      expect(estAlpha?.observable).toBe(true);

      const estBeta = estate.getStatelet('beta');
      expect(estBeta).not.toBeNull();
      expect(estBeta?.name).toBe('beta');
      expect(estBeta?.value).toBe(false);
      expect(estBeta?.observable).toBe(true);

      const estGamma = estate.getStatelet('gamma');
      expect(estGamma).not.toBeNull();
      expect(estGamma?.name).toBe('gamma');
      expect(estGamma?.value).toBe(false);
      expect(estGamma?.observable).toBe(false);
    });

    test('should not get what was not set.', () => {
      const estate = new ExperienceState();
      estate.setStatelet('gamma', false, false);
      estate.setStatelet('alpha', true);
      estate.setStatelet('beta', false);

      const estDelta = estate.getStatelet('delta');
      expect(estDelta).toBeNull();
    });

    test('should be able to set a named value multiple times, but only retrieve the last set instance.', () => {
      const estate = new ExperienceState();
      estate.setStatelet('alpha', true, true);
      estate.setStatelet('alpha', true, false);
      estate.setStatelet('alpha', false, false);

      const estAlpha = estate.getStatelet('alpha');
      expect(estAlpha).not.toBeNull();
      expect(estAlpha?.name).toBe('alpha');
      expect(estAlpha?.value).toBe(false);
      expect(estAlpha?.observable).toBe(false);
    });

    test('should return results by value, so that they\'re safe from manipulation.', () => {
      const estate = new ExperienceState({'alpha': true});
      const estAlphaBefore = estate.getStatelet('alpha');
      expect(estAlphaBefore?.value).toBe(true);

      if (estAlphaBefore) {
        // This will always be safe, or else the test will gave failed by now.
        // We're just keeping TypeScript happy.
        estAlphaBefore.value = false;
      }

      const estAlphaAfter = estate.getStatelet('alpha');
      expect(estAlphaBefore?.value).toBe(false);
      expect(estAlphaAfter?.value).toBe(true);
    });

    test('should set results by value, so that they\'re safe from manipulation.', () => {
      const estate = new ExperienceState({'alpha': true});
      const estBefore = estate.getStatelet('alpha');

      expect(estBefore?.name).toBe('alpha');
      expect(estBefore?.value).toBe(true);

      if (estBefore) {
        estBefore.value = false;
        estate.setStatelet(estBefore);

        estBefore.name = 'gamma';
        estBefore.value = true;
        estBefore.observable = false;
        estate.setStatelet(estBefore);
      }

      const estAlphaAfter = estate.getStatelet('alpha');
      expect(estAlphaAfter?.name).toBe('alpha');
      expect(estAlphaAfter?.value).toBe(false);
      expect(estAlphaAfter?.observable).toBe(true);

      const estGammaAfter = estate.getStatelet('gamma');
      expect(estGammaAfter?.name).toBe('gamma');
      expect(estGammaAfter?.value).toBe(true);
      expect(estGammaAfter?.observable).toBe(false);
    });
  });

  describe('iterator', () => {
    test('should retrieve what was set, and only what was set.', () => {
      const estate = new ExperienceState();
      estate.setStatelet('gamma', false, false);
      estate.setStatelet('alpha', true);
      estate.setStatelet('beta', false);

      const keysFound = [];
      for (let est of estate.statelets) {
        keysFound.push(est.name);
      }

      expect(keysFound).toContain('alpha');
      expect(keysFound).toContain('beta');
      expect(keysFound).toContain('gamma');
      expect(keysFound).toHaveLength(3);
    });

    test('should retrieve iterated statelets by value.', () => {
      const estate = new ExperienceState();
      estate.setStatelet('gamma', true);
      estate.setStatelet('alpha', true);
      estate.setStatelet('beta', true);

      for (let est of estate.statelets) {
        est.value = false;
        const estAfter = estate.getStatelet(est.name);

        expect(estAfter).not.toBeNull();
        expect(estAfter?.value).toBe(true);
      }
    });

    test('should retrieve iterated statelets by value, even if they haven\'t been iterated over yet.', () => {
      const estate = new ExperienceState();
      estate.setStatelet('gamma', true);
      estate.setStatelet('alpha', true);
      estate.setStatelet('beta', true);

      for (let est of estate.statelets) {
        estate.setStatelet('gamma', false);
        estate.setStatelet('alpha', false);
        estate.setStatelet('beta', false);

        expect(est.value).toBe(true);
      }
    });

    test('should iterate stably even if statelets are added during iteration.', () => {
      const estate = new ExperienceState();
      estate.setStatelet('gamma', true);
      estate.setStatelet('alpha', true);
      estate.setStatelet('beta', true);

      let i = 0;
      const names = [];
      for (let est of estate.statelets) {
        i++;
        expect(i).toBeLessThanOrEqual(3);

        const name = est.name;
        names.push(name);
        estate.setStatelet(name + '+1', true);
      }

      expect(names).toHaveLength(3);
    });

    test('should produce stable iteration even if same statelets added in different order.', () => {
      const est1 = new ExperienceState();
      const est2 = new ExperienceState();

      est1.setStatelet('foo');
      est1.setStatelet('bar');
      est1.setStatelet('baz');
      est1.setStatelet('quux');

      est2.setStatelet('quux');
      est2.setStatelet('baz');
      est2.setStatelet('bar');
      est2.setStatelet('foo');

      const names1 = [];
      for (let name of est1.statelets) {
        names1.push(name);
      }
      const names2 = [];
      for (let name of est2.statelets) {
        names2.push(name);
      }
      // Fortunately Jest knows how to test elementwise equality of arrays.
      expect(names1).toEqual(names2);
    });
  })

  describe('equals and clone', () => {
    let estOrig: ExperienceState;
    let estClone: ExperienceState;

    beforeEach(() => {
      estOrig = new ExperienceState({
        'alpha': true,
        'beta': false,
        'gamma': false
      });
      estClone = estOrig.clone();
    });

    test('should equal reciprocally if same statelets set, even in different order.', () => {
      const est1 = new ExperienceState();
      const est2 = new ExperienceState();

      est1.setStatelet('foo');
      est1.setStatelet('bar');
      est1.setStatelet('baz');
      est1.setStatelet('quux');

      est2.setStatelet('quux');
      est2.setStatelet('baz');
      est2.setStatelet('bar');
      est2.setStatelet('foo');

      expect(est1.equals(est2)).toBeTruthy();
      expect(est2.equals(est1)).toBeTruthy();
    });

    test('should produce a clone that is equal to the original.', () => {
      const isEqual = estOrig.equals(estClone);
      expect(isEqual).toBeTruthy();
    });

    test('should no longer be equal if a value is altered.', () => {
      estOrig.setStatelet('gamma', true);
      const isEqual = estOrig.equals(estClone);
      expect(isEqual).toBeFalsy();
    });

    test('should no longer be equal if a value is added to the original.', () => {
      estOrig.setStatelet('delta', true);
      const isEqual = estOrig.equals(estClone);
      expect(isEqual).toBeFalsy();
    });

    test('should no longer be equal if a value is added to the clone.', () => {
      estClone.setStatelet('delta', true);
      const isEqual = estOrig.equals(estClone);
      expect(isEqual).toBeFalsy();
    });

    test('should no longer be equal if an observability is altered.', () => {
      const eslGammaBefore = estOrig.getStatelet('gamma');
      expect(eslGammaBefore?.observable).toBeTruthy();

      estOrig.setStatelet('gamma', false, false);
      const eslGammaAfter = estOrig.getStatelet('gamma');
      expect(eslGammaAfter?.observable).toBeFalsy();

      const isEqual = estOrig.equals(estClone);
      expect(isEqual).toBeFalsy();
    });

    test('should become equal again if values are set to the same thing.', () => {
      estOrig.setStatelet('gamma', true, true);
      estClone.setStatelet('gamma', true, true);
      const isEqual = estOrig.equals(estClone);
      expect(isEqual).toBeTruthy();
    });

    test('should ensure that equality is reciprocal.', () => {
      let isEqual = estClone.equals(estOrig);
      expect(isEqual).toBeTruthy();

      estOrig.setStatelet('gamma', true);
      estClone.setStatelet('delta', true);
      isEqual = estClone.equals(estOrig);
      expect(isEqual).toBeFalsy();
    });

  });

  describe('toString', () => {
    let estOrig: ExperienceState;
    let estClone: ExperienceState;

    beforeEach(() => {
      estOrig = new ExperienceState({
        'alpha': true,
        'beta': false,
        'gamma': false
      });
      estClone = estOrig.clone();
    });

    test('should use toString for string coercion.', () => {
      expect(estOrig.toString()).toEqual(`${estOrig}`);
      expect(estOrig.toString()).toEqual(estOrig + '');
    });

    test('should produce equal string representations if equal.', () => {
      expect(`${estOrig}`).toEqual(`${estClone}`);
    });

    test('should produce unequal string representations if unequal.', () => {
      estClone.setStatelet('foo');
      expect(`${estOrig}`).not.toEqual(`${estClone}`);
    });

    test('should produce equal strings if made equal again.', () => {
      estOrig.setStatelet('foo');
      estClone.setStatelet('bar');
      expect(`${estOrig}`).not.toEqual(`${estClone}`);

      estClone.setStatelet('foo');
      estOrig.setStatelet('bar');
      expect(`${estOrig}`).toEqual(`${estClone}`);
    });

    test('should produce equal strings even if same statelets added in different order.', () => {
      estOrig.setStatelet('foo');
      estOrig.setStatelet('bar');
      estOrig.setStatelet('baz');
      estOrig.setStatelet('quux');

      estClone.setStatelet('quux');
      estClone.setStatelet('baz');
      estClone.setStatelet('bar');
      estClone.setStatelet('foo');

      expect(`${estOrig}`).toEqual(`${estClone}`);
    });
  });
});
