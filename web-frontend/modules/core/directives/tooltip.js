/**
 * This is a very simple and fast tooltip directive. It will add the binding value as
 * tooltip content. The tooltip only shows if there is a value.
 */
export default {
  /**
   * If there is a value and the tooltip has not yet been initialized we can add the
   * mouse events to show and hide the tooltip.
   */
  initialize(el) {
    console.log("initialize")
    el.updatePositionEvent = () => {
      console.log("updatePositionEvent")
      const rect = el.getBoundingClientRect()
      const width = rect.right - rect.left
      el.tooltipElement.style.top = rect.bottom + 4 + 'px'
      el.tooltipElement.style.left = rect.left + width / 2 + 'px'
    }
    el.tooltipMouseEnterEvent = () => {
      console.log("mouseEnterEvent")
      if (el.tooltipElement) {
        this.terminate(el)
      }
      if (el.value) {
        let value = el.value
        el.timeOut = setTimeout(() => {
          console.log("mouseEnterEvent Timeout")
          el.tooltipElement = document.createElement('div')
          el.tooltipElement.className = 'tooltip tooltip--body tooltip--center'
          document.body.insertBefore(el.tooltipElement, document.body.firstChild)

          el.tooltipContentElement = document.createElement('div')
          el.tooltipContentElement.className = 'tooltip__content'
          el.tooltipContentElement.textContent = value
          el.tooltipElement.appendChild(el.tooltipContentElement)

          el.updatePositionEvent()

          // When the user scrolls or resizes the window it could be possible that the
          // element where the tooltip is anchored to has moved, so then the position
          // needs to be updated. We only want to do this when the tooltip is visible.
          window.addEventListener('scroll', el.updatePositionEvent, true)
          window.addEventListener('resize', el.updatePositionEvent)
          el.timeOut = null
        }, el.delay || 0)
      }
    }
    el.tooltipMoveLeaveEvent = () => {
      console.log("moveLeaveEvent")
      if (el.timeOut) {
        clearTimeout(el.timeOut)
        el.timeOut = null
      }
      if (el.tooltipElement) {
        el.tooltipElement.parentNode.removeChild(el.tooltipElement)
        el.tooltipElement = null
        el.tooltipContentElement = null
      }

      window.removeEventListener('scroll', el.updatePositionEvent, true)
      window.removeEventListener('resize', el.updatePositionEvent)
    }
    el.addEventListener('mouseenter', el.tooltipMouseEnterEvent)
    el.addEventListener('mouseleave', el.tooltipMoveLeaveEvent)
  },
  /**
   * If there isn't a value or if the directive is unbinded the tooltipElement can
   * be destroyed if it wasn't already and all the events can be removed.
   */
  terminate(el) {
    console.log("terminate")
    if (el.tooltipElement && el.tooltipElement.parentNode) {
      el.tooltipElement.parentNode.removeChild(el.tooltipElement)
    }
    el.tooltipElement = null
    el.tooltipContentElement = null
    el.removeEventListener('mouseenter', el.tooltipMouseEnterEvent)
    el.removeEventListener('mouseleave', el.tooltipMoveLeaveEvent)
    window.removeEventListener('scroll', el.updatePositionEvent, true)
    window.removeEventListener('resize', el.updatePositionEvent)
  },
  bind(el, binding) {
    console.log("bind")
    el.tooltipElement = null
    el.tooltipContentElement = null
    binding.def.update(el, binding)
  },
  update(el, binding) {
    console.log("update")
    let { value } = binding
    if (value != null && typeof value === 'object') {
      if (value.value === el.value && value.delay === el.delay) {
        return
      }
      el.value = value.value
      el.delay = value.delay || 0
    } else {
      if (value === el.value) {
        return
      }
      el.value = value
    }

    if (!!el.value && el.tooltipElement === null) {
      binding.def.initialize(el)
    } else if (!el.value) {
      binding.def.terminate(el)
    }
  },
  unbind(el, binding) {
    console.log("unbind")
    binding.def.terminate(el)
  },
}
