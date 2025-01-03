import plotly.graph_objects as go

income_sources = [
    'Room and Board Income', 'Care Level Income', 
    'Ancillary Income', 'Other Income'
]
expenses = [
    'Total Nursing Expenses', 'Total Dietery Expenses',
    'Total Housekeeping and Laundry Expenses', 'Total Recreation Expenses',
    'Total Marketing Expenses', 'Total R&M Expenses', 'Outside Ground Services',
    'Utilities', 'Total G&A Expenses', 'Management Fee', 'Real Estate Taxes', 'Operating Income'
]

def total_revenue_stack_line(df):
    # Transpose the DataFrame so time is on x-axis
    df_transposed = df.transpose()
    
    # Create figure
    fig = go.Figure()
    
    # Add a trace for each income source
    for source in income_sources:
        fig.add_trace(go.Scatter(
            x=df_transposed.index[:-1],  # Without the final YTD
            y=df_transposed[source],  # Values for each income source
            name=source,
            stackgroup='one',  # This enables stacking
            fill='tonexty'     # Fill area between traces
        ))
    
    # Add Total Revenue line on top
    fig.add_trace(go.Scatter(
        x=df_transposed.index[:-1],
        y=df_transposed['Total Revenue'],
        name='Total Revenue',
        line=dict(color='black', width=2),
        mode='lines'  # Only show line, no fill
    ))

    # Update layout
    fig.update_layout(
        title_text="Revenue Breakdown Over Time",
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        height=600,
        showlegend=True,
        hovermode='x unified'
    )
    
    return fig

def total_expense_stack_line(df):
        # Transpose the DataFrame so time is on x-axis
    df_transposed = df.transpose()
    
    # Create figure
    fig = go.Figure()
    
    # Add a trace for each income source
    for expense in expenses:
        if expense != 'Operating Income':
            fig.add_trace(go.Scatter(
                x=df_transposed.index[:-1],  # Without the final YTD
                y=df_transposed[expense],  # Values for each income source
                name=expense,
                stackgroup='one',  # This enables stacking
                fill='tonexty'     # Fill area between traces
            ))

    # Update layout
    fig.update_layout(
        title_text="Expense Breakdown Over Time",
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        height=600,
        showlegend=True,
        hovermode='x unified'
    )
    
    return fig

def sankey_diagram(df, font_size=10):
    # Prepare Sankey data
    labels = (income_sources + ['Total Revenue'] + expenses + 
             ['Operating Income'])
    
    # Create source-target pairs
    source = (
        [labels.index(src) for src in income_sources] +  # Income to Total Revenue
        [labels.index('Total Revenue')] * len(expenses)   # Total Revenue to each expense
    )
    
    target = (
        [labels.index('Total Revenue')] * len(income_sources) +  # All income to Total Revenue
        [labels.index(exp) for exp in expenses]  # Total Revenue to each expense
    )
    
    # Calculate values
    values = (
        [df.loc[src].iloc[-1] for src in income_sources] +  # Income values
        [-df.loc[exp].iloc[-1] for exp in expenses]  # Expense values (negative to show outflow)
    )

    def format_value(val):
        val = int(val) if isinstance(val, (int, float)) else val
        abs_val = abs(val)
        if abs_val >= 1_000_000:
            return f"${abs_val/1_000_000:.1f}M"
        elif abs_val >= 1_000:
            return f"${abs_val/1_000:.1f}K"
        else:
            return f"${abs_val:.0f}"
    
    values_ = values.copy()
    values_.insert(len(income_sources), df.loc['Total Revenue'].iloc[-1])
    values_.insert(-1, df.loc['Operating Income'].iloc[-1])

    for i in range(len(labels)):
        labels[i] = f"{labels[i]} ({format_value(values_[i])})"

    # Create Sankey diagram with color differentiation
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            # Color income nodes green, expenses red, and Total Revenue blue
            color=["#009933"] * len(income_sources) + 
                  ["#3f3f3f"] + 
                  ["#cc0000"] * len(expenses) +
                  ["#3498db"],
        ),
        link=dict(
            color=["#efefef"] * len(source),
            source=source,
            target=target,
            value=[abs(v) for v in values],  # Use absolute values for link widths
            label=[format_value(v) for v in values]
        ),
        textfont=dict(color="white", size=font_size)
    )])
    fig.update_layout(
        title_text="Revenue and Expense Flow",
        font_size=font_size,
        height=800  # Make the diagram taller for better visibility
    )

    return fig